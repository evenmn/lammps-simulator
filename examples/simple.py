from vashishta_simulator import Simulator
from vashishta_simulator.computer import CPU

sim = Simulator(directory="simulation")
sim.set_lammps_script("script.in")
sim.run(computer=CPU(num_procs=4, lmp_exec="lmp_mpi"))
