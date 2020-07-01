import os

class Computer:
    """This is the parent computer class, which controls how 
    to run LAMMPS. The required methods are __init__ and __call__
    
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param args: command line arguments
    :type args: dict
    """
    def __init__(self, lmp_exec="lmp_mpi", args={}):
        raise NotImplementedError("Class {} has no instance '__init__'."
                                  .format(self.__class__.__name__))
        
    def __call__(self, lmp_script, var):
        """ Start LAMMPS simulation
        
        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param var: LAMMPS variables defined by the command line
        :type var: dict
        """
        raise NotImplementedError("Class {} has no instance '__call__'."
                                  .format(self.__class__.__name__))
                   
    @staticmethod             
    def run_lammps(num_procs, lmp_exec, lmp_script, args):
        """Run LAMMPS script lmp_script using executable lmp_exec on num_procs 
        processes with command line arguments specified by args
        
        :param num_procs: number of processes
        :type num_procs: int
        :param lmp_exec: LAMMPS executable
        :type lmp_exec: str
        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param args: command line arguments
        :type args: dict
        """
        call_string = f"mpirun -n {num_procs} {lmp_exec} "
        for key1, value1 in args.items():
            for key2, value2 in value1.items():
                call_string += f"{key1} {key2} {value2} "
        call_string += f"-in {lmp_script}"
        return call_string
        
class CPU(Computer):
    """ Run simulations on desk computer. This method runs the executable
        mpirun -n {num_procs} lmp_mpi script.in
    and requires that LAMMPS is built with mpi.
    
    :param num_procs: number of processes. Default 4
    :type num_procs: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param args: command line arguments
    :type args: dict
    """
    def __init__(self, num_procs=4, lmp_exec="lmp_mpi", args={}):
        self.num_procs = num_procs
        self.lmp_exec = lmp_exec
        self.args = args
        
    def __call__(self, lmp_script, var):
        """ Start LAMMPS simulation
        
        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param var: LAMMPS variables defined by the command line
        :type var: dict
        """
        
        var = {"-var" : var}     
        merged_args = {**self.args, **var}
        
        print(merged_args)
        
        call_string = self.run_lammps(self.num_procs, 
                                      self.lmp_exec, 
                                      lmp_script, 
                                      merged_args)
        os.system(call_string)
        
class GPU(Computer):
    """ Run simulations on gpu. 
    
    :param gpus_per_node: GPUs per node
    :type gpus_per_node: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param args: command line arguments
    :type args: dict
    """
    def __init__(self, gpu_per_node=1, lmp_exec="lmp_kokkos_cuda_mpi", args={}):
        self.gpu_per_node = gpu_per_node
        self.lmp_exec = lmp_exec
        
        default_args = {"-pk" : {"kokkos" : "", "newton" : "on", "comm" : "no"},
                        "-k" : {"on" : f"g {self.gpu_per_node}"},
                        "-sf" : {"kk" : ""}}
        self.args = {**default_args, **args}    # merge 
        
        
    def __call__(self, lmp_script, var):
        """ Start LAMMPS simulation
        
        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param var: LAMMPS variables defined by the command line
        :type var: dict
        """
        
        var = {"-var" : var}
                        
        merged_args = {**self.args, **var}
        
        call_string = self.run_lammps(self.gpu_per_node, 
                                      self.lmp_exec, 
                                      lmp_script, 
                                      merged_args)
        os.system(call_string)
        
class SlurmCPU(Computer):
    """ Run LAMMPS simulations on CPU cluster with the Slurm queueing system.
    
    :param num_nodes: number of nodes
    :type num_nodes: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param settings: slurm settings
    :type settings: dict
    :param args: command line arguments
    :type args: dict
    :param procs_per_node: number of processes per node (number of cores)
    :type procs_per_node: int
    :param lmp_module: name of the preferred LAMMPS module
    :type lmp_module: str
    :param jobscript: name of the jobscript
    :type jobscript: str
    """
    def __init__(self, num_nodes,
                       lmp_exec="lmp_mpi",
                       settings={},
                       args={},
                       procs_per_node=16,
                       lmp_module="LAMMPS/13Mar18-foss-2018a",
                       jobscript="jobscript"):
        self.num_nodes = num_nodes
        self.num_procs = num_nodes * procs_per_node
        self.lmp_exec = lmp_exec
        self.lmp_module = lmp_module
        self.jobscript = jobscript
        
        default_settings = {"job-name" : "CPU-job",
                            "account" : "nn9272k",
                            "time" : "05:00:00",
                            "partition" : "normal",
                            "ntasks" : str(self.num_procs),
                            "nodes" : str(self.num_nodes),
                            "output" : "slurm.out",
                            #"mem-per-cpu" : str(3800),
                            #"mail-type" : "BEGIN,TIME_LIMIT_10,END",
                           }
        
        self.settings = {**default_settings, **settings}
        self.args = args
        
    def generate_jobscript(self, lmp_script, args):
        """ Generate jobscript.
        
        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param args: command line arguments
        :type args: dict
        """
                    
        with open(self.jobscript, "w") as f:
            f.write("#!/bin/bash\n\n")
            for key, setting in self.settings.items():
                f.write(f"#SBATCH --{key}={setting}\n#\n")
                
            f.write("## Set up job environment:\n")                                                     
            f.write("source /cluster/bin/jobsetup\n")
            f.write("module purge\n")                                    
            f.write("set -o errexit\n\n")
            f.write(f"module load {self.lmp_module}\n\n")
            f.write(self.run_lammps(self.num_procs, 
                                    self.lmp_exec, 
                                    lmp_script, 
                                    args))
        
    def __call__(self, lmp_script, var):
        """ Start LAMMPS simulation
        
        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param var: LAMMPS variables defined by the command line
        :type var: dict
        """
        
        var = {"-var" : var}
                        
        merged_args = {**self.args, **var}
        
        self.generate_jobscript(lmp_script, merged_args)
        os.system(f"sbatch {self.jobscript}")
        
        
class SlurmGPU(Computer):
    """ Run LAMMPS simulations on GPU cluster with the Slurm queueing system.
    
    :param gpu_per_node: number of GPUs
    :type gpu_per_node: int
    :param lmp_exec: LAMMPS executable
    :type lmp_exec: str
    :param settings: slurm settings
    :type settings: dict
    :param args: command line arguments
    :type args: dict
    :param jobscript: name of the jobscript
    :type jobscript: str
    """
    def __init__(self, gpu_per_node=1, 
                       lmp_exec="lmp_mpi",
                       settings={},
                       args={},
                       jobscript="jobscript"):
        self.gpu_per_node = gpu_per_node
        self.lmp_exec = lmp_exec
        self.jobscript = jobscript
        
        default_settings = {"job-name" : "GPU-job",
                            "partition" : "normal",
                            "ntasks" : str(self.gpu_per_node),
                            "cpus-per-task" : "2",
                            "gres" : "gpu:" + str(self.gpu_per_node),
                            "output" : "slurm.out",
                            #"mem-per-cpu" : str(3800),
                            #"mail-type" : "BEGIN,TIME_LIMIT_10,END",
                           }
                           
        default_args = {"-pk" : {"kokkos" : "", "newton" : "on", "neigh" : "half"},
                        "-k" : {"on" : f"g {self.gpu_per_node}"},
                        "-sf" : {"kk" : ""}}
        self.args = {**default_args, **args}    # merge 
                           
        self.settings = {**default_settings, **settings}
        
        
        
    def generate_jobscript(self, lmp_script, args):
        """ Generate jobscript.
        
        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param args: command line arguments
        :type args: dict
        """
                    
        with open(self.jobscript, "w") as f:
            f.write("#!/bin/bash\n\n")
            for key, setting in self.settings.items():
                f.write(f"#SBATCH --{key}={setting}\n#\n")
                
            f.write("echo $CUDA_VISIBLE_DEVICES\n")                                                     
            f.write(self.run_lammps(self.gpu_per_node, 
                                    self.lmp_exec, 
                                    lmp_script, 
                                    args))   
        
    def __call__(self, lmp_script, var):
        """ Start LAMMPS simulation
        
        :param lmp_script: LAMMPS script
        :type lmp_script: str
        :param var: LAMMPS variables defined by the command line
        :type var: dict
        """
        
        var = {"-var" : var}
                        
        merged_args = {**self.args, **var}
        
        self.generate_jobscript(lmp_script, merged_args)
        os.system(f"sbatch {self.jobscript}")
