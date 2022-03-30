"""
Example on how to submit a CPU job to a cluster using Slurm.
There is also an alternative script that is commented out
which does the same, but where a device is manually defined.

date: March 30th, 2022
"""

from lammps_simulator import Simulator

slurm_args = {'job-name': 'CPU-job',
              'ntasks': 16,
              'nodes': 1}

sim = Simulator(directory="simulation")
sim.set_input_script("in.lammps", temp=300)
sim.run(num_procs=16, slurm=True, slurm_args=slurm_args)

"""
from lammps_simulator import Simulator
from lammps_simulator.device import SlurmCPU

device = SlurmCPU(num_procs=16)
sim = Simulator(directory="simulation")
sim.set_input_script("in.lammps", temp=300)
sim.run(device=device)
"""
