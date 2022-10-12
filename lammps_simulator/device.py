import re
import subprocess
from numpy import ndarray


class Device:
    """Device base class, executing the command

        mpirun -n {num_procs} {lmp_exec} {lmp_script}

    :param num_procs: number of processes, 1 by default
    :type num_procs: int
    :param lmp_exec: LAMMPS executable, 'lmp' by default
    :type lmp_exec: str
    :param lmp_args: LAMMPS command line arguments
    :type lmp_args: dict
    :param slurm: whether or not simulation should be run from Slurm, 'False' by default
    :type slurm: bool
    :param slurm_args: slurm sbatch command line arguments
    :type slurm_args: dict
    :param generate_jobscript: whether or not jobscript should be generated, 'True' by default
    :type generate_jobscript: bool
    :param jobscript: filename of jobscript, 'job.sh' by default
    :type jobscript: str
    """
    def __init__(self, num_procs=1, lmp_exec="lmp", lmp_args={}, slurm=False,
                 slurm_args={}, generate_jobscript=True, jobscript="job.sh",
                 ssh_dir=None):
        self.num_procs = num_procs
        self.lmp_exec = lmp_exec
        self.lmp_args = lmp_args
        self.slurm = slurm
        self.slurm_args = slurm_args
        self.generate_jobscript = generate_jobscript
        self.jobscript = jobscript
        self.ssh_dir = ssh_dir

        if self.ssh_dir is not None:
            self.sendlabel = f"SEND_TO_SSH_"  # prefix of temporary jobscript


    def __str__(self):
        repr = "Custom"
        if self.slurm:
            repr += " (slurm)"
        return repr


    def __call__(self, lmp_script, lmp_var, stdout, stderr):
        """Start LAMMPS simulation

        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param lmp_var: LAMMPS lmp_variables defined by the command line
        :type lmp_var: dict
        :returns: job-ID
        :rtype: int
        """
        self.lmp_args["-in"] = lmp_script

        exec_list = self.get_exec_list(self.num_procs, self.lmp_exec, self.lmp_args, lmp_var)
        if self.slurm:
            if self.ssh_dir is None: # Run locally
                if self.generate_jobscript:
                    self.gen_jobscript(exec_list, self.jobscript, self.slurm_args)
                output = subprocess.check_output(["sbatch", self.jobscript])
            else: # Run on ssh 
                if self.generate_jobscript:
                    self.gen_jobscript(exec_list, self.sendlabel + self.jobscript, self.slurm_args)
                subprocess.run(['rsync', '-av', '--remove-source-files', self.sendlabel + self.jobscript, self.ssh_dir + self.jobscript]) 
                ssh, wd = self.ssh_dir.split(':')
                output = subprocess.check_output(["ssh", ssh, f"cd {wd} && sbatch {self.jobscript}"])
            job_id = int(re.findall("([0-9]+)", str(output))[0])
            print(f"Job submitted with job ID {job_id}")
            return job_id

        else:
            if self.ssh_dir is None: 
                procs = subprocess.Popen(exec_list, stdout=stdout, stderr=stderr)
            else:
                ssh, wd = self.ssh_dir.split(':')
                procs = subprocess.Popen(["ssh", ssh, f"cd {wd} && {' '.join(exec_list)}"], stdout=stdout, stderr=stderr)
            pid = procs.pid
            print(f"Simulation started with process ID {pid}")
            return pid

    @staticmethod
    def get_exec_list(num_procs, lmp_exec, lmp_args, lmp_var):
        """Making a list with all mpirun arguments:

            list = ['mpirun', '-n', {num_procs}, {lmp_exec}, '-in',
                    {lmp_script}, {lmp_args}, {lmp_var}]

        :param num_procs: number of processes
        :type num_procs: int
        :param lmp_exec: LAMMPS executable
        :type lmp_exec: str
        :param lmp_args: LAMMPS command line arguments
        :type lmp_args: dict
        :param lmp_var: LAMMPS variables defined by the command line
        :type lmp_var: dict
        :returns: list with mpirun executables
        :rtype: list of str
        """
        exec_list = ["mpirun", "-n", str(num_procs), lmp_exec]
        for key, value in lmp_args.items():
            exec_list.append(key)
            exec_list.extend(str(value).split())
        for key, value in lmp_var.items():
            # variable may be an LAMMPS index variable
            if type(value) in [list, tuple, ndarray]:
                exec_list.extend(["-var", key])
                exec_list.extend(map(str, list(value)))
            else:
                exec_list.extend(["-var", key, str(value)])
        return exec_list

    @staticmethod
    def gen_jobscript(exec_list, jobscript, slurm_args):
        """Generate jobscript:

            #!/bin/bash
            #SBATCH --{key1}={value1}
            #SBATCH --{key2}={value2}
            ...
            mpirun -n {num_procs} {lmp_exec} -in {lmp_script} {lmp_args} {lmp_var}

        :param exec_list: list of strings to be executed
        :type exec_list: list
        :param jobscript: name of jobscript to be generated
        :type jobscript: str
        :param slurm_args: slurm sbatch command line arguments to be used
        :type slurm_args: dict
        """
        with open(jobscript, "w") as f:
            f.write("#!/bin/bash\n\n")
            for key, setting in slurm_args.items():
                if setting is None:
                    f.write(f"#SBATCH --{key}\n#\n")
                else:
                    f.write(f"#SBATCH --{key}={setting}\n#\n")
            f.write("\n")
            f.write(" ".join(exec_list))


class Custom(Device):
    pass


class CPU(Device):
    def __str__(self):
        return "CPU"


class GPU(Device):
    """Run simulations on gpu.

    :param gpus_per_node: GPUs per node, 1 by default
    :type gpus_per_node: int
    :param mode: GPU mode, has to be either 'kokkos' or 'gpu', 'kokkos' by default
    :type mode: str
    """
    def __init__(self, gpu_per_node=1, mode="kokkos", **kwargs):
        super().__init__(**kwargs)
        self.gpu_per_node = gpu_per_node

        if mode == "kokkos":
            default_lmp_args = {"-pk": "kokkos newton on neigh full",
                                "-k": f"on g {self.gpu_per_node}",
                                "-sf": "kk"}
        elif mode == "gpu":
            default_lmp_args = {"-pk": "gpu newton on neigh full",
                                "-k": f"on g {self.gpu_per_node}",
                                "-sf": "gpu"}
        else:
            raise NotImplementedError

        self.lmp_args = {**default_lmp_args, **self.lmp_args}    # merge

    def __str__(self):
        return "GPU"


class SlurmCPU(Device):
    """Run LAMMPS simulations on CPU cluster with the Slurm queueing system.

    :param procs_per_node: number of processes per node, 16 by default
    :type procs_per_node: int
    """
    def __init__(self, num_nodes, procs_per_node=16, **kwargs):
        super().__init__(**kwargs)
        self.num_nodes = num_nodes
        self.num_procs = num_nodes * procs_per_node

        default_slurm_args = {"job-name": "CPU-job",
                              "partition": "normal",
                              "ntasks": str(self.num_procs),
                              "nodes": str(self.num_nodes),
                              "output": "slurm.out",
                              }

        self.slurm_args = {**default_slurm_args, **self.slurm_args}

    def __str__(self):
        return "CPU (slurm)"


class SlurmGPU(Device):
    """Run LAMMPS simulations on GPU cluster with the Slurm queueing system.

    :param gpu_per_node: number of GPUs
    :type gpu_per_node: int
    :param mode: GPU mode, has to be either 'kokkos' or 'gpu', 'kokkos' by default
    :type mode: str
    """
    def __init__(self, gpu_per_node=1, mode="kokkos", **kwargs):
        super().__init__(**kwargs)
        self.gpu_per_node = gpu_per_node

        default_slurm_args = {"job-name": "GPU-job",
                              "partition": "normal",
                              "ntasks": str(self.gpu_per_node),
                              "cpus-per-task": "2",
                              "gres": "gpu:" + str(self.gpu_per_node),
                              "output": "slurm.out",
                              }

        if mode == "kokkos":
            default_lmp_args = {"-pk": "kokkos newton on neigh full",
                                "-k": f"on g {self.gpu_per_node}",
                                "-sf": "kk"}
        elif mode == "gpu":
            default_lmp_args = {"-pk": "gpu newton on neigh full",
                                "-sf": "gpu"}
        else:
            raise NotImplementedError

        self.lmp_args = {**default_lmp_args, **self.lmp_args}    # merge
        self.slurm_args = {**default_slurm_args, **self.slurm_args}

    def __str__(self):
        return "GPU (slurm)"
