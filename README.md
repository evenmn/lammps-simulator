# LAMMPS simulator
Python package for launching simulations in LAMMPS. The code is oriented around the ```Simulator``` class, which takes a working directory as argument. The simulation is run from the working directory, and the philosophy is that all the files used are copied to this directory.

## Installation
First download the contents:
``` bash
$ git clone https://github.com/evenmn/lammps_simulator.git
```
and then install lammps_simulator:
``` bash
$ cd lammps_simulator
$ pip install .
```

## Basic usage
A simple usage example could look like this:
``` python
from lammps_simulator import Simulator
from lammps_simulator.computer import CPU

sim = Simulator(directory="simulation")
sim.set_input_script("script.in")
sim.run(computer=CPU(num_procs=4, lmp_exec="lmp_mpi"))
```
where the LAMMPS input script ```script.in``` is run from the directory ```simulation``` on 4 CPU processes by calling the LAMMPS executable ```lmp_mpi```.

### Copy to working directory
Often, the LAMMPS script reads other files, like parameter files, data files or other LAMMPS scripts. The function ```copy_to_wd``` can be used to copy any file to the working directory:
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
If your LAMMPS script takes variables, they can be specified by
``` python
sim.set_input_script("script.in", var1=v1, var2=v2, ..., varN=vN)
```

For more examples, see the examples pages and the documentation.
