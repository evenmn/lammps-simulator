from vashishta_simulator import AutoSim
from vashishta_simulator.substance import Silica
from vashishta_simulator.computer import CPU
from vashishta_simulator.directory import Custom

stretch = 2
 
sim = AutoSim(substance=Silica(init_config="system.data"), 
                            directory=Custom(f"stretch{stretch}", overwrite=False),
                            computer=CPU(num_procs=18))
sim.generate_parameter_file("SiO2.vashishta")
sim.set_input_script("script.in")
sim(var={"stretch" : stretch})
