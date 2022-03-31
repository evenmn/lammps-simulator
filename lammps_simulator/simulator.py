import os
import shutil
import warnings
import subprocess


class Simulator:
    """Initialize class

    :param directory: working directory
    :type directory: str
    :param script: LAMMPS input script
    :type script: str
    :param overwrite: whether or not working directory should be overwritten, 'False' by default
    :type overwrite: bool
    :param copy: whether or not input script should be copied to working directory, 'True' by default
    :type copy: bool
    """

    from .computer import Custom

    def __init__(self, directory=None, script=None, overwrite=False, copy=True):
        self.set_wd(directory, overwrite)
        self.set_input_script(script, copy)

    
    def set_wd(self, directory, overwrite=False):
        """Set working directory

        :param directory: working directory
        :type directory: str
        :param overwrite: whether or not working directory should be overwritten, 'False' by default
        :type overwrite: bool
        """
        if directory is None:
            self.wd = None
        else:
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
        :type filename: str or tuple of str
        """
        if self.wd is None:
            warnings.warn("Working directory is not defined!")
        else:
            for file in filename:
                head, tail = os.path.split(file)
                shutil.copyfile(file, self.wd + tail)


    def set_input_script(self, filename, copy=True, **var):
        """Set LAMMPS script

        :param filename: LAMMPS input script
        :type filename: str
        :param var: variables to be specified by the command line
        :type var: unpacked dict
        :param copy: whether or not input script should be copied to working directory, 'True' by default
        :type copy: bool
        """
        self.var = var
        if copy and self.wd is not None:
            head, self.lmp_script = os.path.split(filename)
            shutil.copyfile(filename, self.wd + self.lmp_script)
        else:
            self.lmp_script = filename


    def set_var(**var):
        """Set LAMMPS variables

        :param var: variables to be specified by the command line
        :type var: unpacked dict
        """
        self.var = var


    def run(self, computer=None, device=None, stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE, **kwargs):
        """Run simulation

        :param computer: computer object specifying computation device
        :type computer: obj
        :param stdout: where to write output from LAMMPS simulation. No output to terminal by default.
        :type stdout: subprocess output object
        :param stderr: where to write errors from LAMMPS simulation. Errors are written to terminal by default.
        :type stderr: subprocess output object
        :param kwargs: arguments to be passed to Custom computer. Will only be used if computer=None.
        :type kwargs: unpacked dictionary
        :returns: job-ID
        :rtype: int
        """
        if computer is None and device is None:
            device = self.Custom(**kwargs)
        elif device is None:
            warnings.warn("'Computer' is deprecated from version 1.1.0 and is replaced by the more intuitive 'Device'", DeprecationWarning)
            device = computer
        main_path = os.getcwd()
        if self.wd is not None:
            os.chdir(self.wd)
        job_id = device(self.lmp_script, self.var, stdout, stderr)
        os.chdir(main_path)
        return job_id


    def run_custom(self, stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE, **kwargs):
        """Run Custom simulation

        :param stdout: where to write output from LAMMPS simulation. No output to terminal by default.
        :type stdout: subprocess output object
        :param stderr: where to write errors from LAMMPS simulation. Errors are written to terminal by default.
        :type stderr: subprocess output object
        :param kwargs: arguments to be passed to Custom computer
        :type kwargs: unpacked dictionary
        :returns: job-ID
        :rtype: int
        """
        warnings.warn("'run_custom' is deprecated from version 1.1.0, use 'run' instead", DeprecationWarning)
        computer = self.Custom(**kwargs)
        main_path = os.getcwd()
        if self.wd is not None:
            os.chdir(self.wd)
        job_id = computer(self.lmp_script, self.var, stdout, stderr)
        os.chdir(main_path)
        return job_id
