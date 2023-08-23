Variables
=========

LAMMPS variables can easily be assigned to the input scripts as :code:`set_input_script` variables:

.. code-block:: python

   sim.set_input_script("script.in", var1=v1, var2=v2, ..., varN=vN)

Or one can store the variables in a dictionary and unpack it when calling the function:

.. code-block:: python

   lmp_vars = {'var1': v1, 'var2': v2, ... 'varN': vN}
   sim.set_input_script("script.in", **lmp_vars)

Variables might also be lists (index variables in LAMMPS terms):

.. code-block:: python

   sim.set_input_script("script.in", var=[1, 2, 3])
