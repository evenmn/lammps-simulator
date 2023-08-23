.. _Slurm:

Slurm
======

:code:`lammps-simulator` supports submitting simulations to a queue using Slurm. To do this, simply set :code:`slurm=True`:

.. code-block:: python

   from lammps_simulator import sim

   ...
   sim.run(num_procs=4, lmp_exec="lmp", slurm=True)

This will create a job script, :code:`job.sh`, in the background that is submitted to slurm with the command :code:`sbatch job.sh`. The Slurm arguments can be specified using a dictionary:

.. code-block:: python

   slurm_args={'job-name': 'fun_run',
               'partition': 'normal',
               'nodes': 1,
               'ntasks': 4}

   sim.run(num_procs=4, lmp_exec="lmp", slurm=True, slurm_args=slurm_args)

If the Slurm argument only contains a keyword (e.g. :code:`wait`), set the value to :code:`None`:

.. code-block:: python

   slurm_args={'job-name': 'fun_run',
               'partition': 'normal',
               'nodes': 1,
               'ntasks': 4,
               'wait': None}


Changing name of job script
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To change the name of the generated job script, specify the new name with :code:`jobscript=<new-name>`. To submit an already generated job script, set :code:`generate_jobscript=False`:

.. code-block:: python

   sim.run(num_procs=4, lmp_exec="lmp", slurm=True, generate_jobscript=False, jobscript="another_jobscript.sh")


The :code:`SlurmCPU` device
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, it can be convenient to use the premade Slurm devices, when submitting jobs to the queue using Slurm. These devices contain specific arguments for the device and default Slurm arguments, such that not all the arguments have to be specified manually. :code:`SlurmCPU` take the arguments :code:`num_nodes` and :code:`procs_per_node=16` in addition to the arguments mentioned above, with :code:`num_procs=num_nodes*procs_per_node`. The default arguments are

.. code-block:: python

   default_slurm_args = {"job-name": "CPU-job",
                         "partition": "normal",
                         "ntasks": str(num_procs),
                         "nodes": str(num_nodes),
                         "output": "slurm.out",
                        }

such that they match the number of processes defined elsewhere. They are individually overwritten if another value is set by the user. 


The :code:`SlurmGPU` device
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similarly, :code:`SlurmGPU` takes the additional arguments :code:`gpu_per_node` and :code:`mode="kokkos"`. The default Slurm and LAMMPS arguments for :code:`SlurmGPU` are 

.. code-block:: python

   default_slurm_args = {"job-name": "GPU-job",
                         "partition": "normal",
                         "ntasks": str(self.gpu_per_node),
                         "cpus-per-task": "2",
                         "gres": "gpu:" + str(self.gpu_per_node),
                         "output": "slurm.out",
                        }

   if mode == "kokkos":
       default_lmp_args = {"-pk": "kokkos newton on neigh full",
                           "-k": f"on g {self.gpu_per_node}",
                           "-sf": "kk"}
   elif mode == "gpu":
       default_lmp_args = {"-pk": f"gpu {self.gpu_per_node}",
                           "-sf": "gpu"}

More about LAMMPS arguments on the next page.


Array jobs
^^^^^^^^^^^

Slurm array jobs can also easily be submitted. In the example below, an array of simulations with temperatures ranging from 110 to 150 incremented by 10 is submitted:

.. code-block:: python

   from lammps_simulator import Simulator
   from lammps_simulator.device import SlurmCPU

   slurm_args = {'job-name': 'arrayjob',
                 'nodes': 1,
                 'ntasks': 1,
                 'array': '110-150:10'
   }

   device = SlurmCPU(1, lmp_exec="lmp", slurm_args=slurm_args)

   sim = Simulator(directory="simulation")
   sim.set_input_script("script.in", temp="${SLURM_ARRAY_TASK_ID}")
   sim.run(device=device)


Adding lines to job script
^^^^^^^^^^^^^^^^^^^^^^^^^^

One can pregenerate a job script using

.. code-block:: python

    sim.pre_generate_jobscript(num_procs=4, lmp_exec="lmp", slurm_args = slurm_args)

and then add more lines to the job script before submitting the job:

.. code-block:: python

    sim.add_to_jobscript(" \n line1 \n line2")



