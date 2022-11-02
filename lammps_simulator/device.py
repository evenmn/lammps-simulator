import re
import subprocess
from numpy import ndarray
import os 
import warnings


class Device:
    """Device base class, executing the command

        mpirun -n {num_procs} {lmp_exec} {lmp_script}

    :param num_procs: number of processes, 1 by default.
    :type num_procs: int
    :param lmp_exec: LAMMPS executable, 'lmp' by default.
    :type lmp_exec: str
    :param lmp_args: LAMMPS command line arguments.
    :type lmp_args: dict
    :param slurm: whether or not simulation should be run from Slurm, 'False' by default.
    :type slurm: bool
    :param slurm_args: slurm sbatch command line arguments.
    :type slurm_args: dict
    :param write_jobscript: whether or not to write jobscript, 'True by default'.
    :type write_jobscript: bool
    :param jopscript_name: filename of jobscript, 'job.sh' by default.
    :type jobscript_name: str
    :param execute: whether or not to run the program, 'True' by default.
    :type execute: bool
    :param activate_virtual: Activate virtual cores
    :type activate_virtual: bool
    """
    def __init__(self, num_procs=1, mpi_args={}, lmp_exec="lmp", lmp_args={},
                 slurm=False, slurm_args={}, write_jobscript=True, jobscript_name="job.sh",
                 execute = True, activate_virtual=False):
        
        self.num_procs = num_procs
        self.lmp_exec = lmp_exec
        self.lmp_args = lmp_args
        self.slurm = slurm
        self.slurm_args = slurm_args
        self.write_jobscript = write_jobscript
        self.jobscript_name = jobscript_name 
        self.execute = execute
        self.activate_virtual = activate_virtual
        
        # create default mpirun/mpiexec argument dictionary and merge
        default_mpi_args = {'-n' : num_procs}
        self.mpi_args = {**default_mpi_args, **mpi_args}    # merge
        if activate_virtual:
            hostfile_name = 'hostfile'
            with open(self.wd + '/' + hostfile_name, 'w') as f:
                f.write(f"localhost slots={self.mpi_args['-n']}")
            self.mpi_args['-hostfile'] = hostfile_name


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
        
        if (":" in self.dir):
            self.ssh, self.wd = self.dir.split(":")
        else:
            self.ssh = None
            self.wd = self.dir

        self.lmp_args["-in"] = lmp_script
        exec_list = self.get_exec_list(self.mpi_args, self.lmp_exec, self.lmp_args, lmp_var)
       
        if self.write_jobscript:
            if self.jobscript_string is None:
                self.jobscript_string = self.gen_jobscript_string(exec_list, self.slurm_args)
            if self.ssh is None: # locally stored
                self.store_jobscript(self.jobscript_string, self.wd + '/' + self.jobscript_name)    
            else: # temporary locally stored
                p = subprocess.Popen(['ssh', 'egil', f'cat - > {self.wd}/{self.jobscript_name}'], stdin=subprocess.PIPE)
                p.communicate(input=str.encode(self.jobscript_string))

        if not self.execute: # Option to only generate jobscript
            return 0
        
        if self.slurm: # Run with slurm
            if self.ssh is None: # Run locally
                main_path = os.getcwd()
                os.chdir(self.wd)
                output = subprocess.check_output(["sbatch", self.jobscript_name])
                os.chdir(main_path)
            else: # Run on ssh 
                output = subprocess.check_output(["ssh", self.ssh, f"cd {self.wd} && sbatch {self.jobscript_name}"])
            
            job_id = int(re.findall("([0-9]+)", str(output))[0])
            print(f"Job submitted with job ID {job_id}")
            return job_id
            
      
        else: # Run directly 
            if self.ssh is None: 
                main_path = os.getcwd()
                os.chdir(self.wd)
                procs = subprocess.Popen(exec_list, stdout=stdout, stderr=stderr)
                os.chdir(main_path)
            else:
                procs = subprocess.Popen(["ssh", self.ssh, f"cd {self.wd} && {' '.join(exec_list)}"], stdout=stdout, stderr=stderr)
            pid = procs.pid
            print(f"Simulation started with process ID {pid}")
            return pid
        
        
        
 
    @staticmethod
    def store_jobscript(string, path): 
        # Might find better name but used 'write_jobscript' for bool value
        with open(path, "w") as f:
            f.write(string)
             

    @staticmethod
    def get_exec_list(mpi_args, lmp_exec, lmp_args, lmp_var):
        """Making a list with all mpirun arguments:

            list = ['mpirun', {mpi_args}, {lmp_exec}, '-in',
                    {lmp_script}, {lmp_args}, {lmp_var}]

        :param mpi_args: mpirun/mpiexec command line arguments
        :type mpi_args: dict
        :param lmp_exec: LAMMPS executable
        :type lmp_exec: str
        :param lmp_args: LAMMPS command line arguments
        :type lmp_args: dict
        :param lmp_var: LAMMPS variables defined by the command line
        :type lmp_var: dict
        :returns: list with mpirun executables
        :rtype: list of str
        """
       
        exec_list = ["mpirun"]
        for key, setting in mpi_args.items():
            exec_list.append(key)
            if setting is not None:
                exec_list.extend(str(setting).split())
        exec_list += [lmp_exec]
        for key, setting in lmp_args.items():
            exec_list.append(key)
            if setting is not None:
                exec_list.extend(str(setting).split())
        for key, setting in lmp_var.items():
            # variable may be a LAMMPS index variable
            if type(setting) in [list, tuple, ndarray]:
                exec_list.extend(["-var", key])
                exec_list.extend(map(str, list(setting)))
            else:
                exec_list.extend(["-var", key, str(setting)])
        return exec_list

 

    @staticmethod
    def gen_jobscript_string(exec_list, slurm_args, linebreak = True):  
        """Generate jobscript string:

            #!/bin/bash
            #SBATCH --{key1}={value1}
            #SBATCH --{key2}={value2}
            ...
            mpirun {mpi_args} {lmp_exec} -in {lmp_script} {lmp_args} {lmp_var}

        :param exec_list: list of strings to be executed
        :type exec_list: list
        :param slurm_args: slurm sbatch command line arguments to be used
        :type slurm_args: dict
        """
        
        string = "#!/bin/bash\n\n"
        for key, setting in slurm_args.items():
            if setting is None:
                string += f"#SBATCH --{key}\n#\n"
            else:
                string += f"#SBATCH --{key}={setting}\n#\n"
        string += "\n"
        string += " ".join(exec_list)
        if linebreak:
            string += "\n"
        return string
        


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
