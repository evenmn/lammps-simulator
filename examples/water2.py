from vashishta_simulator import AutoSim
from vashishta_simulator.substance import Water
from vashishta_simulator.computer import CPU, GPU, Slurm_CPU, Slurm_GPU 
from vashishta_simulator.directory import Custom, Verbose
from math import cos, pi

# Set parameters
Z_Hs = [0.50]
thetas = [95]
Bs = [0.4]
Hs = [1.0]
Ds = [0.1]
#lambda4s = [1.4, 1.5, 1.6]

# Simulate
for Z_H in Z_Hs:
  for theta in thetas:
    for B in Bs:
      for H in Hs:
        for D in Ds:
          #for lambda4 in lambda4s:
          Z_O = - 2 * Z_H
          params = {"HHH" : {"Zi" : Z_H, "Zj" : Z_H},
                    "OOO" : {"Zi" : Z_O, "Zj" : Z_O},
                    "HOO" : {"Zi" : Z_H, "Zj" : Z_O, "H" : H, "D" : D},
                    "OHH" : {"Zi" : Z_O, "Zj" : Z_H, "H" : H, "D" : D,  
                             "cos(theta)" : cos(theta * pi / 180), "B" : B}}
                  
          sim = AutoSim(substance=Water(init_config="watercube_4nm.data"), 
                                        directory=Custom("simulation", overwrite=True),
                                        computer=CPU(num_procs=18))
          sim.generate_parameter_file("H2O.vashishta", params=params)
          sim.set_input_script("script.in")
          sim()
