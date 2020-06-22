import os
from shutil import copyfile

class Simulator:
    """ Initialize class
    
    Parameters
    ----------
    substance : obj
        which potential to use
    """
    
    from .computer import CPU
    
    def __init__(self, directory, overwrite=False):
        self.cwd = directory
        if overwrite:
            self.cwd = directory
            try:
                os.makedirs(directory)
            except:
                pass
        else:
            ext = 0
            repeat=True
            while repeat:
                try:
                    os.makedirs(self.cwd)
                    repeat=False
                except FileExistsError:
                    ext += 1
                    self.cwd = directory + f"_{ext}"
        self.cwd += "/"
        
    def copy_to_wd(self, filename):
        """Copy to working directory.
        """
        head, tail = os.path.split(filename)
        copyfile(filename, self.cwd + tail)
        
    def ordered_parameter_string(self, params, param_suffices, param_list, string):
        """ Returning an ordered list of all the parameter values.
        
        Parameters
        ----------
        params : dictionary
            dictionary with all parameters.
        param_suffices : List of str  
            list of all parameter suffices.
        param_list : list   
            initial list to append parameter to.
        string : str
            initial string that will be extended.
        """
        for suffix in param_suffices:
            param_list.append(params[suffix])
        for param in param_list:
            string += str(param) + 2 * " "
        return string + "\n"
        
    def append_type_to_file(self, name, params, filename):
        """ Append the actual parameter values to the parameter file.
        
        Parameters
        ----------
        name : str 
            name of interaction combo (e.g. "SiSiSi")
        params : dictionary 
            dictonary with all parameters
        filename  : str
            filename 
        """
        # Split name
        from re import findall
        prefix_list = findall('[A-Z][^A-Z]*', name)
        params_line1 = ["H", "eta", "Zi", "Zj", "r1s", "D", "r4s"] # correctly ordered
        params_line2 = ["W", "rc", "B", "xi", "r0", "C", "cos(theta)"]  # correctly ordered
        string_line1 = self.ordered_parameter_string(params, params_line1, prefix_list, "")
        string_line2 = self.ordered_parameter_string(params, params_line2, [], (len(name) + 6) * " ")
            
        with open(filename, 'a') as file:
            file.write("\n")
            file.write(string_line1)
            file.write(string_line2)
            
                
    def generate_parameter_file(self, substance, filename="dest.vashishta", params={}):
        """ Generates input parameter file for the potential. The default
        parameters are the ones specified in Wang et al., so parameters
        that are not specified will fall back on these default parameters.
        
        Parameters
        ----------
        filename : str   
            filename
        header_filename : str  
            header file name
        """
        # Get default parameters
        if substance == "water":
            from .substance import water
            self.params = water
        elif substance == "silica":
            from .substance import silica
            self.params = silica
        else:
            raise NotImplemented
        
        # Set parameters
        for comb, parameters in params.items():
            for parameter, value in parameters.items():
                self.params[comb][parameter] = value
        
        # Make new parameter file
        this_dir, this_filename = os.path.split(__file__)
        header_filename = this_dir + "/data/header.vashishta"
        self.param_file = filename
        
        copyfile(header_filename, self.cwd + self.param_file)
        
        # Add parameters to file
        for name, params in self.params.items():
            self.append_type_to_file(name, params, self.cwd + self.param_file)
            
    def set_parameter_file(self, filename, copy=True):
        """Set parameter file that is already prepared.
        """
        if copy:
            head, self.param_file = os.path.split(filename)
            copyfile(filename, self.cwd + self.param_file)
        else:
            self.param_file = filename

    def set_lammps_script(self, filename, var={}, copy=True):
        """Set LAMMPS script
        """
        self.var = var
        if copy:
            head, self.lmp_script = os.path.split(filename)
            copyfile(filename, self.cwd + self.lmp_script)
        else:
            self.lmp_script = filename
            
    def run(self, computer=CPU(num_procs=4), jobscript=None):
        """Run simulation
        """
        main_path = os.getcwd()
        os.chdir(self.cwd)
        computer(self.lmp_script, self.var)
        os.chdir(main_path)
        
        
if __name__ == "__main__":

    # EXAMPLE USAGE
    from computer import CPU
    
    sim = Simulator(directory="test", overwrite=True)
    sim.copy_to_wd("watercube_4nm.data")
    sim.generate_parameter_file("water", filename="H2O.vashishta", params={})
    sim.set_lammps_script("script.in", var = {}, copy=True)
    sim.run(computer=CPU(num_procs=4), jobscript=None)
    
    
    
