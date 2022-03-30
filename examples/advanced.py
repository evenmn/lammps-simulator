"""
This is an example on how to sim a script where both
the simulator and device objects are manually defined.

date: March 30th, 2022
"""

from lammps_simulator import Simulator
from lammps_simulator.device import GPU

device = GPU(lmp_exec="lmp", gpus_per_node=1)

var = {"run_time": 3000,
       "temp": 300,
       "pressure": 1}

sim = Simulator(directory="simulation", overwrite=True)
sim.copy_to_wd("FField.reax.FC", "init_config.data", "compute_chem_pot.in")
sim.set_input_script("script.in", copy=True, **var)
sim.run(device=device)
