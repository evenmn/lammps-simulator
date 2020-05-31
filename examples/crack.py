from vashishta_simulator import AutoSim
from vashishta_simulator.substance import Silica
from vashishta_simulator.computer import CPU
from vashishta_simulator.directory import Custom

import numpy as np
stretches = np.arange(2.25, 5.0, 0.25)

for stretch in stretches:
    sim = AutoSim(substance=Silica(init_config="../restart/wedgeBeta_notch_nodefects_576000.restart"), 
                                directory=Custom(f"../data/stretch{stretch}_wedgeBeta_notch_nodefects_576000", overwrite=True),
                                computer=CPU(num_procs=18))
    sim.generate_parameter_file("SiO2.vashishta")
    sim.set_input_script("../lammps/script.in")
    sim(var={"stretch" : stretch})
