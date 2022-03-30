from setuptools import setup

setup(name='lammps-simulator',
      version='1.1.0',
      description='Python interface for running LAMMPS input scripts',
      url='http://github.com/evenmn/lammps-simulator',
      author='Even Marius Nordhagen',
      author_email='evenmn@mn.uio.no',
      license='MIT',
      packages=['lammps_simulator'],
      include_package_data=True,
      zip_safe=False)
