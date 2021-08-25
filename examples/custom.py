from lammps_simulator import Simulator

sim = Simulator(directory="simulation")
sim.set_input_script("in.lammps")
sim.run_custom(num_procs=4, lmp_exec="lmp", stdout=None)

