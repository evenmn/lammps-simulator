from lammps_simulator import Simulator
from lammps_simulator.computer import CPU

sim = Simulator(directory="simulation")
sim.set_input_script("script.in")
sim.run(computer=CPU(num_procs=4, lmp_exec="lmp_mpi"))
