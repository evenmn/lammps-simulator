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

Other devices include :code:`GPU` (run LAMMPS with the :code:`GPU` or :code:`KOKKOS` package), :code:`SlurmCPU` (submit LAMMPS CPU jobs to Slurm) and :code:`SlurmGPU` (submit LAMMPS GPU jobs to Slurm). The Slurm support is further described in the Slurm-section.


