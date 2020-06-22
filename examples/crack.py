from vashishta_simulator import Simulator
from vashishta_simulator.computer import CPU

import numpy as np
stretches = np.arange(3.25, 5.0, 0.25)

for stretch in stretches:
    sim = Simulator(directory="crack_simulation", overwrite=True)
    sim.copy_to_wd("beta-cristobalite.data")
    sim.generate_parameter_file("silica", filename="SiO2.vashishta")
    sim.set_lammps_script("run.in", var = {"stretch" : stretch})
    sim.run(computer=CPU(num_procs=4))
