"""
This example shows how a 'Device' object can be created to
run LAMMPS. This can be useful when running several simulations
from the same device. Also, the particular device objects often
have better default settings than the 'Custom' device.

date: March 30th, 2022
"""

from lammps_simulator import sim
from lammps_simulator.device import CPU

device = CPU(num_procs=4, lmp_exec="lmp")
sim.set_input_script("script.in")
sim.run(device=device)

