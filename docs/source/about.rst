About
=====

:code:`lammps-simulator` is a package for lauching pre-written LAMMPS scripts from Python, and does not support modifications of the script itself. LAMMPS command line arguments are supported. The desired hardware to be used for the simulation can easily be specified through LAMMPS arguments. Support for Slurm for queue management. 

A simple usage example is presented below where the LAMMPS input script :code:`script.in` is executed through the LAMMPS executable :code:`lmp` which runs 4 parallel processes using the message parsing interface (MPI):

.. code-block:: python

   from lammps_simulator import sim

   sim.set_input_script("script.in")
   sim.run(num_procs=4, lmp_exec="lmp")
