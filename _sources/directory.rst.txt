Simulation directory
====================

If one wants to specify the simulation directory, a custom :code:`Simulator` object has to be created

.. code-block:: python

   from lammps_simulator import Simulator

   sim = Simulator(directory="simulation", overwrite=False)

By setting :code:`overwrite=False`, an extention is added to the directory name if a directory with the same name exists. This is the default behavior, and one should be careful setting :code:`overwrite=True`.

Using a remote directory
^^^^^^^^^^^^^^^^^^^^^^^^^

The simulation can also be executed on a remote server. We follow the same convention as :code:`rsync` and :code:`scp`, and separate the host and directory by a colon:

.. code-block:: python

   from lammps_simulator import Simulator

   sim = Simulator(directory="<hostname>:~/simulation")

Then, files are copied using :code:`rsync` and commands are run remotely using :code:`ssh <hostname> <command>`.

Copy files to directory
^^^^^^^^^^^^^^^^^^^^^^^^

Often, the LAMMPS script requires other files, like parameter files, data files or other LAMMPS scripts. The function :code:`copy_to_wd` can be used to copy any file to the working directory:

.. code-block:: python

    sim.copy_to_wd("parameters.vashishta")
    sim.copy_to_wd("pos.data")
    sim.copy_to_wd("compute_something.in")

or more compact:

.. code-block:: python

    sim.copy_to_wd("parameters.vashishta", "pos.data", "compute_something.in")


Creating sub directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, it is also convenient to create sub directories inside the working directory. This could, for instance, be used to store output files. The syntax for this is similar as for :code:`copy_to_wd` presented above:

.. code-block:: python

   sim.create_subdir("subdir1", "subdir2")


Avoid copying LAMMPS script
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The main idea of the package is to store all the dependencies in the simulation directory, such that the simulation can easily be rerun without being affected by files outside the directory. The dependency files might include data files, parameter files, job scripts, and LAMMPS input script. However, sometimes we do not want to copy the input script, but instead specify the relative path to the input script. To do this, set :code:`copy=False`:

.. code-block:: python

   sim.set_input_script("../script.in", copy=False)
