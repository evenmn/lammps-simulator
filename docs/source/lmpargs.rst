LAMMPS arguments
================

:code:`lammps-simulator` can take a dictionary of LAMMPS arguments as input:

.. code-block:: python

   lmp_args = {'-sf': 'kokkos'}

   sim.run(num_procs=4, lmp_exec="lmp", lmp_args=lmp_args)


