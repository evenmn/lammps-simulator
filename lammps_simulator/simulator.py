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

    from .device import Device

    def __init__(self, directory='.', overwrite=False):
        self.jobscript_string = None # Option to store jobscript in simulator class
        self.full_dir = directory
        
        if (":" in directory):
            self.ssh, self.wd = directory.split(":")
        else:
            self.ssh = None
            self.wd = directory
        if overwrite:
            self._make_dir(self.wd, self.ssh)
        else:
            ext = 0
            repeat = True
            original_dir = self.wd
            while repeat:
                repeat = self._make_dir(self.wd, self.ssh)
                if repeat:
                    ext += 1
                    self.wd = original_dir + f"_{ext}"
        self.wd += "/"

    @staticmethod
    def _make_dir(dir_, host):
        """Make directory, which might be on a remote node

        :param dir_: directory
        :type dir_: str
        :param host: base host for simulation
        :type host: str
        :returns: True if directory exists, False if not
        :rtype: bool
        """
        try:
            if host is None:
                os.makedirs(dir_)
            else:
                res = subprocess.Popen(['ssh', host, 'mkdir', dir_], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = res.communicate()
                if "File exists" in str(error): 
                    raise FileExistsError
        except FileExistsError:
            return True
        return False
        

    def copy_to_wd(self, *filename):
        """Copy one or several files to working directory.

        :param filename: filename or tuple of filenames to copy
        :type filename: str or tuple of str
        """
        if self.wd is None:
            warnings.warn("Working directory is not defined!")
        else:
            for file in filename:
                head, tail = os.path.split(file)
                if self.ssh is None:
                    try:
                        shutil.copyfile(file, self.wd + tail)
                    except shutil.SameFileError:
                        pass
                else:
                    # use subprocess.run for transfer to finish before moving on
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
            for dir_ in dirname:
                self._make_dir(self.wd + dir_, self.ssh)
                        

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
                try:
                    shutil.copyfile(filename, self.wd + self.lmp_script)
                except shutil.SameFileError:
                    pass
            else:
                subprocess.run(['rsync', '-av', filename, self.ssh + ':' + self.wd + self.lmp_script]) 
                
        else:
            self.lmp_script = filename


    def run(self, computer=None, device=None, stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE, activate_virtual=False, **kwargs):
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
            device = self.Device(**kwargs)
        elif device is None:
            warnings.warn("'Computer' is deprecated from version 1.1.0 and is replaced by the more intuitive 'Device'", DeprecationWarning)
            device = computer
        
        device.dir = self.full_dir
        device.ssh = self.ssh
        device.jobscript_string = self.jobscript_string
        job_id = device(self.lmp_script, self.var, stdout, stderr)   
        try: 
            if kwargs['execute'] == False:
                print("Simulation.run() finished with \'execute = False\'")
        except KeyError:
            pass
        
        return job_id

   
    def pre_generate_jobscript(self, **kwargs):
        """ Pre-generate jobscript string from available information
            from self.sim_settings and kwargs.
            
        :param kwargs: arguments to be added to self.sim_settings before generating jobscript string.
        :type kwargs: unpacked dictionary 
        """
            
        #self.set_run_settings(**kwargs)
        #self.sim_settings = {'lmp_args': {}} | self.sim_settings  # Python 3.9 feature
        #self.sim_settings = {'lmp_args': {}, **self.sim_settings}
        #self.sim_settings['lmp_args']['-in'] = self.lmp_script
        
        exec_list = self.Device.get_exec_list(kwargs['mpi_args'] , kwargs['lmp_exec'], kwargs['lmp_args'], self.var)
        self.jobscript_string = self.Device.gen_jobscript_string(exec_list, kwargs['slurm_args'])
     
   
    def add_to_jobscript(self, string, linebreak = True):
        """ Add a string to already exisitng self.jobscript_string.
        
        :param string: String to be added to self.jobscript_string
        :type string: str
        :param linebreak: whether or not to add linebreak after string, 'True' by default. 
        :type linebreak: bool
        """ 
        assert(isinstance(self.jobscript_string, str)), "Cannot add to jobscript when not initialized"
        self.jobscript_string += string
        if linebreak: 
            self.jobscript_string += "\n"
      

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
