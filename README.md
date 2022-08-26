# LAMMPS simulator
A light-weight Python package for launching LAMMPS simulations. Given a LAMMPS input script, the simulation is launched from a specified working directory. The default behavior is to copy the input script and all dependencies to the working directory, making it easy to redo the simulations. Simulations can be submitted directly to the Slurm simulation queue.

## Installation
Install package from source using pip:
``` bash
$ pip install lammps-simulator
```

## Prerequisites
1. Python 3.3+ (subprocess.DEVNULL from 3.3 needed)
2. [LAMMPS](https://lammps.sandia.gov/) (Any recent version)

## Basic usage
To run a LAMMPS script from the current directory, the script has to be specified and the way of running the simulation has to be defined. The easiest way of doing this is to use the default simulation object, `sim`:
``` python
from lammps_simulator import sim

sim.set_input_script("script.in")
sim.run(num_procs=4, lmp_exec="lmp")
```
where the LAMMPS input script ```script.in``` is launched on 4 CPU processes by calling the LAMMPS executable ```lmp```. This corresponds to running
``` bash
$ mpirun -n 4 lmp -in script.in
```

### Defining working directory and copy files to it
Associating each simulation with a respective working directory is good practice, as it makes it easy to rerun the simulation. Create a simulator object associated with a directory by:
``` python
from lammps_simulator import Simulator

sim = Simulator("simulation", overwrite=False)
```
The argument `overwrite` can be set to True if the contents of the simulation should overwrite a potentially existing simulation directory. 

Often, the LAMMPS script requires other files, like parameter files, data files or other LAMMPS scripts. The function ```copy_to_wd``` can be used to copy any file to the working directory:
``` python
sim.copy_to_wd("parameters.vashishta")
sim.copy_to_wd("pos.data")
sim.copy_to_wd("compute_something.in")
```
or more compact:
``` python
sim.copy_to_wd("parameters.vashishta", "pos.data", "compute_something.in")
```

### Assign variables to LAMMPS script
If your LAMMPS script takes command line variables, they can be specified by
``` python
sim.set_input_script("script.in", var1=v1, var2=v2, ..., varN=vN)
```
or

``` python
lmp_vars = {'var1': v1, 'var2': v2, ... 'varN': vN}
sim.set_input_script("script.in", **lmp_vars)
```

Variables might also be lists (index variables in LAMMPS terms):
``` python
sim.set_input_script("script.in", var=[1, 2, 3])
```

### Slurm support
Simulations can be submitted to the Slurm queue by adding `slurm=True` and Slurm arguments to the `run`-method. Basic example:
``` python
slurm_args = {'job-name'='cpu', 'partition'='normal', 'ntasks'=16, 'nodes'=1}
sim.run(num_procs=16, lmp_exec="lmp", slurm=True, slurm_args=slurm_args)
```
A job script, `job.sh`, will then be generated in the simulation directory, which is executed with
```
sbatch job.sh
```

For more examples, see the examples pages and the [documentation](https://evenmn.github.io/lammps-simulator/).
