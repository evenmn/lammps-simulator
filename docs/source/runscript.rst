Running a LAMMPS script
=======================

The simplest way of running a LAMMPS script is through the pre-made :code:`sim` simulation object. A LAMMPS simulation with the script :code:`script.in` can then be launched using

.. code-block:: python

   from lammps_simulator import sim

   sim.set_input_script("script.in")
   sim.run(num_procs=4, lmp_exec="lmp")


Device object
^^^^^^^^^^^^^^^^^^^

Sometimes it can be useful to define a :code:`Device` object, especially when running various simulations with the same hardware specifications. Different devices can be found in :code:`lammps_simulator.device`:

.. code-block:: python

   from lammps_simulator.device import CPU

   device = CPU(num_procs=4, lmp_exec="lmp")
   sim.run(device=device)

Other devices include :code:`GPU` (run LAMMPS with the :code:`GPU` or :code:`KOKKOS` package), :code:`SlurmCPU` (submit LAMMPS CPU jobs to Slurm) and :code:`SlurmGPU` (submit LAMMPS GPU jobs to Slurm). The Slurm support is further described in the `Slurm`_-section.

.. _activate virtual cores:

Activate virtual cores
^^^^^^^^^^^^^^^^^^^^^^^^

In Open MPI version >= 3.0, oversubscription of slots is not allowed by default. One can overcome this by manually bumping up the number of slots. There are multiply ways of doing this, but arguably the easiest way is to make a host file:

.. code-block:: bash

    $ cat hostfile
    localhost slots=<new-number-of-slots>

and then pass it as an argument to :code:`mpirun`/:code:`mpiexec`:

.. code-block:: bash

    mpirun -n 1 -hostfile hostfile ...

By doing this, a simulation can be run both on the physical and the virtual cores of a node, which may give a significant speed-up. In :code:`lammps-simulator`, oversubscribing is built-in with the argument :code:`activate_virtual`:

.. code-block:: python

   from lammps_simulator import sim

   sim.set_input_script("script.in")
   sim.run(num_procs=4, lmp_exec="lmp", activate_virtual=True)

For more information about MPI command line arguments, see `command line arguments`_.
