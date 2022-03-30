"""
In this example, we run an array job doing a temperature grid search for
temperatures 100, 110, 120, 130, 140 and 150. ${SLURM_ARRAY_TASK_ID} is the
array job task ID, which can be passed into the LAMMPS script as an argument. 
Limit the number of tasks, num,  that run at once by adding '%num' to the array
argument. Example: 'array': '100-150:10%10' for 10 jobs at once.

date: March 30th, 2022
"""

from lammps_simulator import Simulator
from lammps_simulator.device import SlurmCPU

slurm_args = {'job-name': 'arrayjob',
              'nodes': 1,
              'ntasks': 1,
              'array': '110-150:10'
}

device = SlurmCPU(1, lmp_exec="lmp", slurm_args=slurm_args)

sim = Simulator(directory="simulation")
sim.set_input_script("script.in", temp="${SLURM_ARRAY_TASK_ID}")
sim.run(device=device)
