import os
import shutil
import warnings
import subprocess


class Simulator:
    """Initialize class

    :param directory: working directory
    :type directory: str
    :param overwrite: whether or not working directory should be overwritten, 'False' by default
    :type overwrite: bool
    """

    # from .computer import Custom
    from .device import Custom # Shouldn't we use this when Computer is deprecated 

    def __init__(self, directory=None, overwrite=False, ssh=None):
        self.ssh = ssh
        if directory is None:
            self.wd = None
        else:
            self.wd = directory
            if overwrite:
                try:
                    if ssh is None:
                        os.makedirs(directory)
                    else:
                        res = subprocess.Popen(['ssh', ssh, 'mkdir', directory], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
                        output, error = res.communicate()
                        if "File exists" in str(error): 
                            raise FileExistsError
                except FileExistsError:
                    pass
            else:
                ext = 0
                repeat = True
                while repeat:
                    try:
                        if ssh is None: 
                            os.makedirs(self.wd)
                        else:
                            res = subprocess.Popen(['ssh', ssh, 'mkdir', self.wd], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
                            output, error = res.communicate()
                            if "File exists" in str(error): 
                                raise FileExistsError
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
                if self.ssh is None:
                    shutil.copyfile(file, self.wd + tail)
                else:
                    # use subprocess.run for transfer to finsih before moving on
                    subprocess.run(['rsync', '-av', file, self.ssh + ':' + self.wd + tail]) 
                    

    def create_subdir(self, *dirname):
        """Create a subdirectory inside the working directory,
        for example to store output data in.

        :param dirname: name of subdirectory to create
        :type filename: str or tuple of str
        """

        if self.wd is None:
            warnings.warn("Working directory is not defined!")
        else:
            for dir in dirname:
                os.makedirs(self.wd + dir)

    def set_input_script(self, filename, copy=True, **var):
        """Set LAMMPS script

        :param filename: LAMMPS input script
        :type filename: str
        :param var: variables to be specified by the command line
        :type var: dict
        :param copy: whether or not input script should be copied to working directory, 'True' by default
        :type copy: bool
        """
        self.var = var
        if copy and self.wd is not None:
            head, self.lmp_script = os.path.split(filename)
            if self.ssh is None:
                shutil.copyfile(filename, self.wd + self.lmp_script)
            else:
                subprocess.run(['rsync', '-av', filename, self.ssh + ':' + self.wd + self.lmp_script]) 
                
        else:
            self.lmp_script = filename


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
            device = self.Custom(**kwargs, ssh_dir = self.ssh + ':' + self.wd) # Go in here
        elif device is None:
            warnings.warn("'Computer' is deprecated from version 1.1.0 and is replaced by the more intuitive 'Device'", DeprecationWarning)
            device = computer
        main_path = os.getcwd()
        
        if self.ssh is None:
            if self.wd is not None:
                os.chdir(self.wd)
            job_id = device(self.lmp_script, self.var, stdout, stderr)
            os.chdir(main_path)
        else:
            job_id = device(self.lmp_script, self.var, stdout, stderr)
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
