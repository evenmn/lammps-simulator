# LAMMPS simulator
A light-weight Python package for launching LAMMPS simulations. Given a LAMMPS input script, the simulation is launched from a specified working directory. The default behavior is to copy the input script and all dependencies to the working directory, making it easy to redo the simulations.

## Installation
Install package using pip:
``` bash
$ pip install git+https://github.com/evenmn/lammps-simulator
```

## Prerequisites
1. Python 3.3+ (subprocess.DEVNULL from 3.3 needed)
2. [LAMMPS](https://lammps.sandia.gov/) (Any recent version)

## Basic usage
The code is oriented around the `Simulator` class, which takes the working directory as argument. Below follows a simple usage example:
``` python
from lammps_simulator import Simulator
from lammps_simulator.computer import CPU

sim = Simulator(directory="simulation")
sim.set_input_script("script.in")
sim.run(computer=CPU(num_procs=4, lmp_exec="lmp_mpi"))
```
where the LAMMPS input script ```script.in``` is launched from the directory ```simulation``` on 4 CPU processes by calling the LAMMPS executable ```lmp_mpi```.

### Copy to working directory
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

Variables might also be lists (index variables in LAMMPS terms).
``` python
sim.set_input_script("script.in", var=[1, 2, 3])
```

For more examples, see the examples pages and the documentation.
