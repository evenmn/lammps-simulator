# Vashishta simulator
Python package for lauching simulations in LAMMPS. The current version supports the Vashishta potential only, but can easily be extended to other potentials. The code is oriented around the ```Simulator``` class, which takes a working directory as argument. The simulation is run from the working directory, and the philosophy is that all the files used are copied to this directory.

## Installation
First download the contents:
``` bash
$ git clone https://github.com/evenmn/vashishta_simulator.git
```
and then install vashishta_simulator:
``` bash
$ cd vashishta_simulator
$ pip3 install .
```

## Usage
Vashishta-simulator is typically used like the following example:
``` python
from vashishta_simulator import Simulator
from vashishta_simulator.computer import CPU
    
sim = Simulator(directory="water_simulation", overwrite=True)
sim.copy_to_wd("watercube_4nm.data")
sim.generate_parameter_file("water", filename="H2O.vashishta")
sim.set_lammps_script("script.in")
sim.run(computer=CPU(num_procs=4))
```

### The ```Simulator``` class
``` python
vashishta_simulator.Simulator(directory, overwrite=False)
```

The ```Simulator``` class takes the preferred working directory as input, and an argument telling whether or not the directory should be overwritten if exists. A number extension is added to avoid the existing directory being overwritten.

### The ```copy_to_wd``` method
``` python
vashishta_simulator.Simulator.copy_to_wd(self, filename)
```
The ```copy_to_wd``` method copies a file to the working directory. The filename is kept.

### The ```set_parameter_file``` method
``` python
vashishta_simulator.Simulator.set_parameter_file(self, filename, copy=True)
```
The ```set_parameter_file``` method takes the preferred parameter file as input. If ```copy``` is true, the parameter file is copied to the working directory. Otherwise, the relative path to the parameter file is used. 

### The ```generate_parameter_file``` method
``` python
vashishta_simulator.Simulator.generate_parameter_file(self, substance, filename, params={})
```
The ```generate_parameter_file``` method generates a parameter file, ```filename```, based on a set of default parameters associated with ```substance```. The Default parameters might be changed using the ```params``` argument. 

### The ```set_lammps_script``` method
``` python
vashishta_simulator.Simulator.set_lammps_script(self, filename, var={}, copy=True)
```
The ```set_lammps_script``` method is used to specify which LAMMPS script that should be used (```filename```). This can either be copied to the working directory (```copy=True```) or not. Command line arguments are specified by ```var```. 

### The ```run``` method
``` python
vashishta_simulator.Simulator.run(self, computer=CPU(num_procs=4), jobscript=None)
```
The ```run``` method is used to run the LAMMPS script. The ```computer``` argument specifies where and how to run the script. Possible methods are ```CPU```, ```GPU```, ```SlurmCPU``` and ```SlurmGPU```, and are provided by the ```Computer``` class. 
