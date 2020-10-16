from lammps_simulator import Simulator
from lammps_simulator.computer import GPU

computer = GPU(lmp_exec="lmp_kokkos_cuda_mpi", gpus_per_node=1)

var = {"run_time": 3000,
       "temp": 300,
       "pressure": 1}

sim = Simulator(directory="simulation", overwrite=True)
sim.copy_to_wd("FField.reax.FC", "init_config.data", "compute_chem_pot.in")
sim.set_input_script("../script.in", copy=True, **var)
sim.run(computer=computer)
