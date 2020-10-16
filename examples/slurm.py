from lammps_simulator import Simulator
from lammps_simulator.computer import SlurmGPU

slurm_args = {"job-name": "GPU-job",
              "partition": "normal",
              "ntasks": 1,
              "cpus-per-task": "2",
              "gres": "gpu:1",
              "output": "slurm.out",
              }

lmp_args = {"-pk": "kokkos newton on comm no",
            "-k": "on g 1",
            "-sf": "kk"}

computer = SlurmGPU(lmp_exec="lmp_kokkos_cuda_mpi",
                    slurm_args=slurm_args,
                    lmp_args=lmp_args,
                    jobscript="job.sh")

var = {"run_time": 3000,
       "temp": 300,
       "pressure": 1}

sim = Simulator(directory="simulation")
sim.copy_to_wd("init_config.data")
sim.set_input_script("script.in", **var)
sim.run(computer=computer)
