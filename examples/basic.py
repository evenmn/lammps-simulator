"""
Basic example script where LAMMPS script 'script.in' is
run in the current directory with the executable 'lmp'
on 4 CPU processes.

date: March 30th, 2022
"""

from lammps_simulator import sim

sim.set_input_script("script.in")
sim.run(num_procs=4, lmp_exec="lmp")
