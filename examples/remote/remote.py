from lammps_simulator import Simulator

sim = Simulator("egil:~/simulation")

sim.set_input_script("in.lammps", length=20)
sim.create_subdir("dump")
sim.copy_to_wd("remote.py")

sim.run(lmp_exec="lmp", num_procs=4)
