import os

class Computer:
    """ """
    def __init__(self):
        raise NotImplementedError("Class {} has no instance '__init__'."
                                  .format(self.__class__.__name__))
        
    def __call__(self):
        raise NotImplementedError("Class {} has no instance '__init__'."
                                  .format(self.__class__.__name__))
        
class CPU(Computer):
    """ Run simulations on desk computer. This method runs the executable
        mpirun -n {num_threads} lmp_mpi script.in
    and requires that LAMMPS is built with mpi.
    
    Parameters
    ----------
    num_threads : int
        number of threads used in the simulation
    """
    def __init__(self, num_procs=4):
        self.num_procs = num_procs
        
    def __call__(self, lmp_script, var):
        """ Run LAMMPS executable. 
        
        Parameters
        ----------
        path : str
            path to working directory
        """
        call_string = f"mpirun -n {self.num_procs} " 
        for key, value in var.items():
            call_string += f"-var {key} {value} "
        call_string += f"lmp_daily -in {lmp_script}"
        os.system(call_string)
        
class GPU(Computer):
    """ Run simulations on gpu. This method runs the executable
        lmp_kokkos_cuda_mpi -pk kokkos newton on comm no -k on g {gpu_per_node}
        -sf kk -in script.in
    and requires that LAMMPS is built with mpi.
    
    Parameters
    ----------
    num_threads : int
        number of threads used in the simulation
    """
    def __init__(self, gpu_per_node=1):
        self.gpu_per_node = gpu_per_node
        
    def __call__(self, path, lmps_script):
        """ Run LAMMPS executable. 
        
        Parameters
        ----------
        path : str
            path to working directory
        """
        from os import getcwd, chdir, system
        main_path = getcwd()
        chdir(path)
        call_string = "lmp_kokkos_cuda_mpi -pk kokkos newton on comm no -k on \
                       g {} -sf kk -in {}" \
                      .format(self.gpu_per_node, lmps_script)
        system(call_string)
        chdir(main_path)
        
class Slurm_CPU(Computer):
    """ Run LAMMPS simulations on CPU cluster with the Slurm queueing system.
    
    Parameters
    ----------
    num_nodes : int
        number of nodes to be used. Assuimg that a node has 16 cores. 
        A normal partition requires num_nodes >= 4
    time : str
        string specifies the maximal wall clock time. Format hh:mm:ss.
    account : str
        cluster account. Format nnXXXXk.
    lmps_module : str
        name of LAMMPS module on cluster.
    jobscript : str
        name of jobscript
        
    Default parameters are appropriate for the Fram cluster
    """
    def __init__(self, num_nodes=4, 
                       time="05:00:00", 
                       account="nn9272k",
                       lmps_module="LAMMPS/13Mar18-foss-2018a",
                       jobscript="jobscript"):
        self.num_nodes = num_nodes
        self.num_threads = num_nodes * 16
        self.time = time
        self.account = account
        self.lmps_module = lmps_module
        self.jobscript = jobscript
        
    def generate_jobscript(self, lmps_script):
        """ Generate jobscript.
        """
        
        settings = {"job-name" : "ParamSearch",
                    "account" : self.account,
                    "time" : self.time,
                    "partition" : "normal",
                    "ntasks" : str(self.num_threads),
                    "nodes" : str(self.num_nodes),
                    "output" : "slurm.out",
                    #"mem-per-cpu" : str(3800),
                    #"mail-type" : "BEGIN,TIME_LIMIT_10,END",
                    }
                    
        temp = "#SBATCH --{}={}\n#\n"
                    
        f = open(self.jobscript, "w")
        f.write("#!/bin/bash\n\n")
        for key, setting in settings.items():
            f.write(temp.format(key, setting))
            
        f.write("## Set up job environment:\n")                                                     
        f.write("source /cluster/bin/jobsetup\n")
        f.write("module purge\n")                                    
        f.write("set -o errexit\n\n")
        f.write("module load {}\n\n".format(self.lmps_module))
        f.write("mpirun lmp_mpi -in {}".format(lmps_script))
            
        f.close()          
        
    def __call__(self, path, lmps_script):
        """ Submit slurm job. 
        
        Parameters
        ----------
        path : str
            path to working directory
        jobscript : str
            jobscript name
        script : str
            LAMMPS infile name
        """
        from os import getcwd, chdir, system
        main_path = getcwd()
        chdir(path)
        self.generate_jobscript(lmps_script)
        system("sbatch {}".format(self.jobscript))
        chdir(main_path)
        
        
class Slurm_GPU(Computer):
    """ Run LAMMPS simulations on GPU cluster with the Slurm queueing system.
    
    Parameters
    ----------
    gpu_per_node : int
        number of cpus per node
    jobscript : str
        name of jobscript
        
    Default parameters are appropriate for the BigFacet cluster
    """
    def __init__(self, gpu_per_node=1, 
                       jobscript="jobscript"):
        self.gpu_per_node = gpu_per_node
        self.jobscript = jobscript
        
    def generate_jobscript(self, lmps_script):
        """ Generate jobscript.
        """
        
        settings = {"job-name" : "ParamSearch",
                    "partition" : "normal",
                    "ntasks" : "1",
                    "cpus-per-task" : "2",
                    "gres" : "gpu:" + str(self.gpu_per_node),
                    "output" : "slurm.out",
                    #"mem-per-cpu" : str(3800),
                    #"mail-type" : "BEGIN,TIME_LIMIT_10,END",
                    }
                    
        temp = "#SBATCH --{}={}\n#\n"
                    
        f = open(self.jobscript, "w")
        f.write("#!/bin/bash\n\n")
        for key, setting in settings.items():
            f.write(temp.format(key, setting))
            
        f.write("echo $CUDA_VISIBLE_DEVICES\n")                                                     
        f.write("mpirun -n {} lmp -k on g {} -sf kk -pk kokkos newton on neigh half -in {}"
                 .format(self.gpu_per_node, self.gpu_per_node, lmps_script))
            
        f.close()          
        
    def __call__(self, path, lmps_script):
        """ Submit slurm job. 
        
        Parameters
        ----------
        path : str
            path to working directory
        jobscript : str
            jobscript name
        script : str
            LAMMPS infile name
        """
        from os import getcwd, chdir, system
        main_path = getcwd()
        chdir(path)
        self.generate_jobscript(lmps_script)
        system("sbatch {}".format(self.jobscript))
        chdir(main_path)
