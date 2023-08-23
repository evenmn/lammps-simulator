.. _command line arguments:

Command line arguments
======================

When launching a LAMMPS simulation, the general command

.. code-block:: bash

    mpirun <mpi_args> <lmp_exec> <lmp_args>

is executed. :code:`mpi_args` usually contains the flag :code:`-n <num_procs>`, and :code:`-hostfile hostfile` is added if :code:`activate_virtual=True` (see :ref:`activate virtual cores`). For the LAMMPS command line arguments :code:`lmp_args`, the flag :code:`-in <lmp_exec>` is always included, with :code:`lmp_exec` being the LAMMPS executable. How to pass custom MPI and LAMMPS arguments is described below.


MPI arguments
^^^^^^^^^^^^^^

MPI arguments can be passed as a dictionary to the :code:`run`-method:

.. code-block:: python

    mpi_args = {'-display-allocation': None,
                '-do-not-launch': None,
                '--timeout': 600}

    sim.run(num_procs=4, lmp_exec="lmp", mpi_args=mpi_args)


LAMMPS arguments
^^^^^^^^^^^^^^^^^

:code:`lammps-simulator` can take a dictionary of LAMMPS arguments as input:

.. code-block:: python

   lmp_args = {'-sf': 'kokkos'}

   sim.run(num_procs=4, lmp_exec="lmp", lmp_args=lmp_args)


