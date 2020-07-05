from vashishta_simulator import Simulator
from vashishta_simulator.computer import CPU, SlurmCPU, SlurmGPU
    
sim = Simulator(directory="water_simulation", overwrite=True)
sim.copy_to_wd("watercube_4nm.data")
sim.generate_parameter_file("water", filename="H2O.vashishta", params={"global" : {"Z_H" : 0.45},
                                                                       "all" : {"rc" : 5.5},
                                                                       "OHH,HOO" : {"H" : 0.6}})
print(sim.params)
sim.set_lammps_script("script.in", var={"heat_time" : 3000})
sim.run(computer=CPU(num_procs=4, lmp_exec="lmp_mpi", args={"-log" : "log"}))
