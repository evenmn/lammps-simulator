import re
import subprocess
from numpy import ndarray


class Computer:
    """Computer base class, which controls how to run LAMMPS.
    The required methods are __init__ and __call__.

    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param lmp_args: LAMMPS command line arguments
    :type lmp_args: dict
    """
    def __init__(self, lmp_exec="lmp", lmp_args={}):
        raise NotImplementedError("Class {} has no instance '__init__'."
                                  .format(self.__class__.__name__))

    def __call__(self, lmp_script, lmp_var):
        """Start LAMMPS simulation

        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param lmp_var: LAMMPS lmp_variables defined by the command line
        :type lmp_var: dict
        :returns: job-ID
        :rtype: int
        """
        raise NotImplementedError("Class {} has no instance '__call__'."
                                  .format(self.__class__.__name__))

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
                f.write(f"#SBATCH --{key}={setting}\n#\n")
            f.write("\n")
            f.write(" ".join(exec_list))


class Custom(Computer):
    """Run simulations. This method runs the executable

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
    def __init__(self, num_procs=1, lmp_exec="lmp", lmp_args={},
                 slurm=False, slurm_args={}, generate_jobscript=True,
                 jobscript="job.sh"):
        self.num_procs = num_procs
        self.lmp_exec = lmp_exec
        self.lmp_args = lmp_args
        self.slurm = slurm
        self.slurm_args = slurm_args
        self.generate_jobscript = generate_jobscript
        self.jobscript = jobscript

    def __str__(self):
        repr = "Custom"
        if self.slurm:
            repr += " (slurm)"
        return repr

    def __call__(self, lmp_script, lmp_var, stdout, stderr):
        self.lmp_args["-in"] = lmp_script

        exec_list = self.get_exec_list(self.num_procs, self.lmp_exec, self.lmp_args, lmp_var)
        if self.slurm:
            if self.generate_jobscript:
                self.gen_jobscript(exec_list, self.jobscript, self.slurm_args)
            output = str(subprocess.check_output(["sbatch", self.jobscript]))
            job_id = int(re.findall("([0-9]+)", output)[0])
        else:
            procs = subprocess.Popen(exec_list, stdout=stdout, stderr=stderr)
            job_id = procs.pid
        print(f"Simulation started with job ID {job_id}")
        return job_id


class CPU(Computer):
    """Run simulations on desk computer. This method runs the executable

        mpirun -n {num_procs} {lmp_exec} {lmp_script}

    and requires that LAMMPS is built with mpi.

    :param num_procs: number of processes, 4 by default
    :type num_procs: int
    :param lmp_exec: LAMMPS executable, 'lmp' by default
    :type lmp_exec: str
    :param lmp_args: LAMMPS command line arguments
    :type lmp_args: dict
    """
    def __init__(self, num_procs=4, lmp_exec="lmp", lmp_args={}):
        self.num_procs = num_procs
        self.lmp_exec = lmp_exec
        self.lmp_args = lmp_args
        self.slurm = False

    def __str__(self):
        return "CPU"

    def __call__(self, lmp_script, lmp_var, stdout, stderr):
        self.lmp_args["-in"] = lmp_script

        exec_list = self.get_exec_list(self.num_procs, self.lmp_exec, self.lmp_args, lmp_var)
        procs = subprocess.Popen(exec_list, stdout=stdout, stderr=stderr)
        job_id = procs.pid
        print(f"Simulation started with job ID {job_id}")
        return job_id


class GPU(Computer):
    """Run simulations on gpu.

        mpirun -n {num_procs} {lmp_exec} {lmp_script}

    :param gpus_per_node: GPUs per node, 1 by default
    :type gpus_per_node: int
    :param lmp_exec: LAMMPS executable, 'lmp' by default
    :type lmp_exec: str
    :param lmp_args: LAMMPS command line arguments
    :type lmp_args: dict
    :param mode: GPU mode, has to be either 'kokkos' or 'gpu', 'kokkos' by default
    :type mode: str
    """
    def __init__(self, gpu_per_node=1, lmp_exec="lmp", lmp_args={},
                 mode="kokkos"):
        self.gpu_per_node = gpu_per_node
        self.lmp_exec = lmp_exec
        self.slurm = False

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

        self.lmp_args = {**default_lmp_args, **lmp_args}    # merge

    def __str__(self):
        return "GPU"

    def __call__(self, lmp_script, lmp_var, stdout, stderr):
        self.lmp_args["-in"] = lmp_script

        exec_list = self.get_exec_list(self.gpu_per_node, self.lmp_exec, self.lmp_args, lmp_var)
        procs = subprocess.Popen(exec_list, stdout=stdout, stderr=stderr)
        job_id = procs.pid
        print(f"Simulation started with job ID {job_id}")
        return job_id


class SlurmCPU(Computer):
    """Run LAMMPS simulations on CPU cluster with the Slurm queueing system.
    Generates jobscript consisting of sbatch command line arguments and
    ends with

        mpirun -n {num_procs} {lmp_exec} {lmp_script}

    The generated jobscript is then executed by sbatch:

        sbatch {jobscript}

    :param num_nodes: number of nodes
    :type num_nodes: int
    :param lmp_exec: LAMMPS executable, 'lmp' by default
    :type lmp_exec: str
    :param lmp_args: LAMMPS command line arguments
    :type lmp_args: dict
    :param slurm_args: slurm sbatch command line arguments
    :type slurm_args: dict
    :param procs_per_node: number of processes per node, 16 by default
    :type procs_per_node: int
    :param generate_jobscript: whether or not jobscript should be generated, 'True' by default
    :type generate_jobscript: bool
    :param jobscript: filename of jobscript, 'job.sh' by default
    :type jobscript: str
    """
    def __init__(self, num_nodes, lmp_exec="lmp", lmp_args={}, slurm_args={},
                 procs_per_node=16, generate_jobscript=True,
                 jobscript="job.sh"):
        self.num_nodes = num_nodes
        self.num_procs = num_nodes * procs_per_node
        self.lmp_exec = lmp_exec
        self.generate_jobscript = generate_jobscript
        self.jobscript = jobscript
        self.slurm = True

        default_slurm_args = {"job-name": "CPU-job",
                              "partition": "normal",
                              "ntasks": str(self.num_procs),
                              "nodes": str(self.num_nodes),
                              "output": "slurm.out",
                              }

        self.slurm_args = {**default_slurm_args, **slurm_args}
        self.lmp_args = lmp_args

    def __str__(self):
        return "CPU (slurm)"

    def __call__(self, lmp_script, lmp_var, stdout, stderr):
        self.lmp_args["-in"] = lmp_script

        if self.generate_jobscript:
            exec_list = self.get_exec_list(self.num_procs, self.lmp_exec, self.lmp_args, lmp_var)
            self.gen_jobscript(exec_list, self.jobscript, self.slurm_args)
        output = str(subprocess.check_output(["sbatch", self.jobscript], stderr=stderr))
        job_id = int(re.findall("([0-9]+)", output)[0])
        print(f"Simulation started with job ID {job_id}")
        return job_id


class SlurmGPU(Computer):
    """Run LAMMPS simulations on GPU cluster with the Slurm queueing system.
    Generates jobscript consisting of sbatch command line arguments and
    ends with

        mpirun -n {num_procs} {lmp_exec} {lmp_script}

    The generated jobscript is then executed by sbatch:

        sbatch {jobscript}

    :param gpu_per_node: number of GPUs
    :type gpu_per_node: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param lmp_args: LAMMPS command line arguments
    :type lmp_args: dict
    :param slurm_args: slurm sbatch command line arguments
    :type slurm_args: dict
    :param generate_jobscript: whether or not jobscript should be generated, 'True' by default
    :type generate_jobscript: bool
    :param jobscript: filename of jobscript, 'job.sh' by default
    :type jobscript: str
    """
    def __init__(self, gpu_per_node=1, lmp_exec="lmp", lmp_args={},
                 slurm_args={}, generate_jobscript=True, jobscript="job.sh",
                 mode="kokkos"):
        self.gpu_per_node = gpu_per_node
        self.lmp_exec = lmp_exec
        self.generate_jobscript = generate_jobscript
        self.jobscript = jobscript
        self.slurm = True

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
                                "-k": f"on g {self.gpu_per_node}",
                                "-sf": "gpu"}
        else:
            raise NotImplementedError

        self.lmp_args = {**default_lmp_args, **lmp_args}    # merge
        self.slurm_args = {**default_slurm_args, **slurm_args}

    def __str__(self):
        return "GPU (slurm)"

    def __call__(self, lmp_script, lmp_var, stdout, stderr):
        self.lmp_args["-in"] = lmp_script

        if self.generate_jobscript:
            exec_list = self.get_exec_list(self.gpu_per_node, self.lmp_exec, self.lmp_args, lmp_var)
            self.gen_jobscript(exec_list, self.jobscript, self.slurm_args)
        output = str(subprocess.check_output(["sbatch", self.jobscript], stderr=stderr))
        job_id = int(re.findall("([0-9]+)", output)[0])
        print(f"Simulation started with job ID {job_id}")
        return job_id
