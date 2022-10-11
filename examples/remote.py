from lammps_simulator import Simulator

sim = Simulator("egil:~/simulation")

sim.set_input_script("script.in")
sim.create_subdir("dump")
sim.copy_to_wd("remote.py")
