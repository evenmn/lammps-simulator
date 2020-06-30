from vashishta_simulator import Simulator
from vashishta_simulator.computer import CPU
    
sim = Simulator(directory="water_simulation", overwrite=True)
sim.copy_to_wd("watercube_4nm.data")
sim.generate_parameter_file("water", filename="H2O.vashishta", params={"OOO" : {"H" : 1965}})
sim.set_lammps_script("script.in", var={"heat_time" : 3000})
sim.run(computer=CPU(num_procs=18, lmp_exec="lmp_daily", args={"-log" : {"log" : ""}}))
