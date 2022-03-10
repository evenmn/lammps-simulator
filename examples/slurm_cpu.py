from lammps_simulator import Simulator
from lammps_simulator.computer import SlurmCPU

computer = SlurmCPU(1, lmp_exec="lmp")

sim = Simulator(directory="simulation")
sim.set_input_script("in.lammps", temp=300)
sim.run(computer=computer)
