from setuptools import setup
#import lammps_simulator

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='lammps-simulator',
      version="1.3.1", #lammps_simulator.__version__,
      description='Python interface for running LAMMPS input scripts',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/evenmn/lammps-simulator',
      author='Even Marius Nordhagen',
      author_email='evenmn@mn.uio.no',
      license='MIT',
      packages=['lammps_simulator'],
      install_requires=['numpy'],
      include_package_data=True,
      zip_safe=False)
