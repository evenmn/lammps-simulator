import os
import shutil


class Simulator:
    """Initialize class

    :param directory: working directory
    :type directory: str
    :param overwrite: if True, a directory with identical name will be overwritten. If False, a number extension is added to the directory name to avoid overwriting
    :type overwrite: bool
    """

    from .computer import CPU

    def __init__(self, directory, overwrite=False):
        self.wd = directory
        if overwrite:
            try:
                os.makedirs(directory)
            except FileExistsError:
                pass
        else:
            ext = 0
            repeat = True
            while repeat:
                try:
                    os.makedirs(self.wd)
                    repeat = False
                except FileExistsError:
                    ext += 1
                    self.wd = directory + f"_{ext}"
        self.wd += "/"

    def copy_to_wd(self, *filename):
        """Copy one or several files to working directory.

        :param filename: filename or list of filenames to copy
        :type filename: str or list of str
        """

        for file in filename:
            head, tail = os.path.split(file)
            shutil.copyfile(file, self.wd + tail)

    def set_input_script(self, filename, copy=True, **var):
        """Set LAMMPS script

        :param filename: LAMMPS input script
        :type filename: str
        :param var: variables to be specified by the command line
        :type var: dict
        :param copy: if True, the file is copied to the working directory
        :type copy: bool
        """
        self.var = var
        if copy:
            head, self.lmp_script = os.path.split(filename)
            shutil.copyfile(filename, self.wd + self.lmp_script)
        else:
            self.lmp_script = filename

    def run(self, computer=CPU(num_procs=4)):
        """Run simulation

        :param computer: how to run the simulation, see computer.py for opt
        :type computer: obj
        """
        main_path = os.getcwd()
        os.chdir(self.wd)
        job_id = computer(self.lmp_script, self.var)
        os.chdir(main_path)
        return job_id
