import re
import subprocess


class Computer:
    """This is the parent computer class, which controls how
    to run LAMMPS. The required methods are __init__ and __call__

    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param lmp_args: command line arguments
    :type lmp_args: dict
    """
    def __init__(self, lmp_exec="lmp_mpi", lmp_args={}):
        raise NotImplementedError("Class {} has no instance '__init__'."
                                  .format(self.__class__.__name__))

    def __call__(self, lmp_script, lmp_var):
        """ Start LAMMPS simulation

        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param lmp_var: LAMMPS lmp_variables defined by the command line
        :type lmp_var: dict
        """
        raise NotImplementedError("Class {} has no instance '__call__'."
                                  .format(self.__class__.__name__))

    @staticmethod
    def get_exec_list(num_procs, lmp_exec, lmp_args, lmp_var):
        """Run LAMMPS script lmp_script using executable lmp_exec on num_procs
        processes with command line arguments specified by lmp_args

        :param num_procs: number of processes
        :type num_procs: int
        :param lmp_exec: LAMMPS executable
        :type lmp_exec: str
        :param lmp_args: command line arguments
        :type lmp_args: dict
        :param lmp_var: lmp_variables defined by the command line
        :type lmp_var: dict
        """
        exec_list = ["mpirun", "-n", str(num_procs), lmp_exec]
        for key, value in lmp_args.items():
            exec_list.extend([key, str(value)])
        for key, value in lmp_var.items():
            exec_list.extend(["-var", str(value)])
        return exec_list

    @staticmethod
    def gen_jobscript(exec_list, jobscript, slurm_args):
        """Generate jobscript.

        :param exec_list: list of strings to be executed
        :type exec_list: list
        :param jobscript: name of jobscript to be generated
        :type jobscript: str
        :param slurm_args: slurm arguments to be used
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

    :param num_procs: number of processes. Default 4
    :type num_procs: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param lmp_args: command line arguments
    :type lmp_args: dict
    """
    def __init__(self, num_procs=1, lmp_exec="lmp_mpi", lmp_args={},
                 slurm=False, slurm_args={}, generate_jobscript=True,
                 jobscript="jobscript"):
        self.num_procs = num_procs
        self.lmp_exec = lmp_exec
        self.lmp_args = lmp_args
        self.slurm = slurm
        self.slurm_args = slurm_args
        self.generate_jobscript = generate_jobscript
        self.jobscript = jobscript

    def __str__(self):
        repr = "General"
        if self.slurm:
            repr += "(slurm)"
        return repr

    def __call__(self, lmp_script, lmp_var):
        self.lmp_args["-in"] = lmp_script

        exec_list = self.get_exec_list(self.num_procs, self.lmp_exec, self.lmp_args, lmp_var)
        if self.slurm:
            if self.generate_jobscript:
                self.gen_jobscript(exec_list, self.jobscript, self.slurm_args)
            output = subprocess.check_output(["sbatch", self.jobscript])
            job_id = int(re.findall("([0-9]+)", output)[0])
            return job_id
        else:
            subprocess.run(exec_list, shell=True)


class CPU(Computer):
    """ Run simulations on desk computer. This method runs the executable
        mpirun -n {num_procs} lmp_mpi script.in
    and requires that LAMMPS is built with mpi.

    :param num_procs: number of processes. Default 4
    :type num_procs: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param lmp_args: command line arguments
    :type lmp_args: dict
    """
    def __init__(self, num_procs=4, lmp_exec="lmp_mpi", lmp_args={}):
        self.num_procs = num_procs
        self.lmp_exec = lmp_exec
        self.lmp_args = lmp_args
        self.slurm = False

    def __str__(self):
        return "CPU"

    def __call__(self, lmp_script, lmp_var):
        self.lmp_args["-in"] = lmp_script

        exec_list = self.get_exec_str(self.num_procs, self.lmp_exec, self.lmp_args, lmp_var)
        subprocess.run(exec_list, shell=True)


class GPU(Computer):
    """ Run simulations on gpu.

    :param gpus_per_node: GPUs per node
    :type gpus_per_node: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param lmp_args: command line arguments
    :type lmp_args: dict
    :param mode: GPU mode, has to be either 'kokkos' or 'gpu'
    :type mode: str
    """
    def __init__(self,
                 gpu_per_node=1,
                 lmp_exec="lmp_kokkos_cuda_mpi",
                 lmp_args={},
                 mode="kokkos"):
        self.gpu_per_node = gpu_per_node
        self.lmp_exec = lmp_exec
        self.slurm = False

        if mode == "kokkos":
            default_lmp_args = {"-pk": "kokkos newton on comm no",
                                "-k": f"on g {self.gpu_per_node}",
                                "-sf": "kk"}
        elif mode == "gpu":
            default_lmp_args = {"-pk": "gpu newton on comm no",
                                "-k": f"on g {self.gpu_per_node}",
                                "-sf": "gpu"}
        else:
            raise NotImplementedError

        self.lmp_args = {**default_lmp_args, **lmp_args}    # merge

    def __str__(self):
        return "GPU"

    def __call__(self, lmp_script, lmp_var):
        self.lmp_args["-in"] = lmp_script

        exec_list = self.get_exec_str(self.num_procs, self.lmp_exec, self.lmp_args, lmp_var)
        subprocess.run(exec_list, shell=True)


class SlurmCPU(Computer):
    """ Run LAMMPS simulations on CPU cluster with the Slurm queueing system.

    :param num_nodes: number of nodes
    :type num_nodes: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param lmp_args: command line arguments
    :type lmp_args: dict
    :param slurm_args: slurm settings
    :type slurm_args: dict
    :param procs_per_node: number of processes per node (number of cores)
    :type procs_per_node: int
    :param lmp_module: name of the preferred LAMMPS module
    :type lmp_module: str
    :param generate_jobscript: if True, a job script is generated
    :type generate_jobscript: bool
    :param jobscript: name of the jobscript
    :type jobscript: str
    """
    def __init__(self,
                 num_nodes,
                 lmp_exec="lmp_mpi",
                 lmp_args={},
                 slurm_args={},
                 procs_per_node=16,
                 lmp_module="LAMMPS/13Mar18-foss-2018a",
                 generate_jobscript=True,
                 jobscript="jobscript"):
        self.num_nodes = num_nodes
        self.num_procs = num_nodes * procs_per_node
        self.lmp_exec = lmp_exec
        self.lmp_module = lmp_module
        self.generate_jobscript = generate_jobscript
        self.jobscript = jobscript
        self.slurm = True

        default_slurm_args = {"job-name": "CPU-job",
                              "account": "nn9272k",
                              "time": "05:00:00",
                              "partition": "normal",
                              "ntasks": str(self.num_procs),
                              "nodes": str(self.num_nodes),
                              "output": "slurm.out",
                              }

        self.slurm_args = {**default_slurm_args, **slurm_args}
        self.lmp_args = lmp_args

    def __str__(self):
        return "CPU cluster"

    def gen_jobscript_(self, lmp_args, lmp_var):
        """ Generate jobscript.

        :param lmp_args: command line arguments
        :type lmp_args: dict
        :param lmp_var: LAMMPS lmp_variables defined by the command line
        :type lmp_var: dict
        """

        with open(self.jobscript, "w") as f:
            f.write("#!/bin/bash\n\n")
            for key, setting in self.slurm_args.items():
                f.write(f"#SBATCH --{key}={setting}\n#\n")

            f.write("## Set up job environment:\n")
            f.write("source /cluster/bin/jobsetup\n")
            f.write("module purge\n")
            f.write("set -o errexit\n\n")
            f.write(f"module load {self.lmp_module}\n\n")
            f.write(self.get_exec_str(self.num_procs, self.lmp_exec, lmp_args, lmp_var))

    def __call__(self, lmp_script, lmp_var):
        self.lmp_args["-in"] = lmp_script

        if self.generate_jobscript:
            exec_list = self.get_exec_str(self.num_procs, self.lmp_exec, self.lmp_args, lmp_var)
            self.gen_jobscript(exec_list, self.jobscript, self.slurm_args)
        output = subprocess.check_output(["sbatch", self.jobscript])
        job_id = int(re.findall("([0-9]+)", output)[0])
        return job_id


class SlurmGPU(Computer):
    """ Run LAMMPS simulations on GPU cluster with the Slurm queueing system.

    :param gpu_per_node: number of GPUs
    :type gpu_per_node: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param lmp_args: command line arguments
    :type lmp_args: dict
    :param slurm_args: slurm settings
    :type slurm_args: dict
    :param generate_jobscript: if True, a job script is generated
    :type generate_jobscript: bool
    :param jobscript: name of the jobscript
    :type jobscript: str
    :param mode: GPU mode, has to be either 'kokkos' or 'gpu'
    :type mode: str
    """
    def __init__(self,
                 gpu_per_node=1,
                 lmp_exec="lmp",
                 lmp_args={},
                 slurm_args={},
                 generate_jobscript=True,
                 jobscript="jobscript",
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
            default_lmp_args = {"-pk": "kokkos newton on comm no",
                                "-k": f"on g {self.gpu_per_node}",
                                "-sf": "kk"}
        elif mode == "gpu":
            default_lmp_args = {"-pk": "gpu newton on comm no",
                                "-k": f"on g {self.gpu_per_node}",
                                "-sf": "gpu"}
        else:
            raise NotImplementedError

        self.lmp_args = {**default_lmp_args, **lmp_args}    # merge

        self.slurm_args = {**default_slurm_args, **slurm_args}

    def __str__(self):
        return "GPU cluster"

    def gen_jobscript_(self, lmp_args, lmp_var):
        """ Generate jobscript.

        :param lmp_args: command line arguments
        :type lmp_args: dict
        :param lmp_var: LAMMPS lmp_variables defined by the command line
        :type lmp_var: dict
        """

        with open(self.jobscript, "w") as f:
            f.write("#!/bin/bash\n\n")
            for key, setting in self.slurm_args.items():
                f.write(f"#SBATCH --{key}={setting}\n#\n")

            f.write("echo $CUDA_VISIBLE_DEVICES\n")
            f.write(self.get_exec_str(self.gpu_per_node, self.lmp_exec, lmp_args, lmp_var))

    def __call__(self, lmp_script, lmp_var):
        self.lmp_args["-in"] = lmp_script

        if self.generate_jobscript:
            exec_list = self.get_exec_list(self.gpu_per_node, self.lmp_exec, self.lmp_args, lmp_var)
            self.gen_jobscript(exec_list, self.jobscript, self.slurm_args)
        output = subprocess.check_output(["sbatch", self.jobscript])
        job_id = int(re.findall("([0-9]+)", output)[0])
        return job_id
