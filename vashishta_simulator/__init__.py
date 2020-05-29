""" Simulation interface for LAMMPS using the Vashishta potential.
Prerequisites include a recent version of LAMMPS with the manybody
package built and Python 3.x. For example usage, see bottom.

@author Even Marius Nordhagen
"""
import os
from shutil import copyfile

class AutoSim:

    from .computer import CPU
    from .directory import Custom
    def __init__(self, substance, directory=Custom("simulation", overwrite=False), computer=CPU(num_procs=4)):
        """ Initialize class
        
        Parameters
        ----------
        substance : obj
            which potential to use
        """
        self.substance = substance
        self.params, self.masses = substance()
        self.pwd = directory(self.params) + "/"
        self.computer=computer
        
        head, self.data_file = os.path.split(substance.init_config)
        copyfile(substance.init_config, self.pwd + self.data_file)
        
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
        params_line1 = ["H", "eta", "Zi", "Zj", "lambda1", "D", "lambda4"] # correctly ordered
        params_line2 = ["W", "rc", "B", "gamma", "r0", "C", "cos(theta)"]  # correctly ordered
        string_line1 = self.ordered_parameter_string(params, params_line1, prefix_list, "")
        string_line2 = self.ordered_parameter_string(params, params_line2, [], (len(name) + 6) * " ")
            
        with open(filename, 'a') as file:
            file.write("\n")
            file.write(string_line1)
            file.write(string_line2)
            
                
    def generate_parameter_file(self, filename="dest.vashishta", params={}):
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
        
        # Set parameters
        for comb, parameters in params.items():
            for parameter, value in parameters.items():
                self.params[comb][parameter] = value
        
        this_dir, this_filename = os.path.split(__file__)
        header_filename = this_dir + "/data/header.vashishta"
        self.param_file = filename
        
        # Add header to file
        copyfile(header_filename, self.pwd + self.param_file)
        
        # Add parameters to file
        for name, params in self.params.items():
            self.append_type_to_file(name, params, self.pwd + self.param_file)
            
    def set_parameter_file(self, filename):
        """Set parameter file that is already prepared.
        """
        head, self.param_file = os.path.split(filename)
        copyfile(filename, self.pwd + self.param_file)
        
    def generate_input_script(self):
        pass
        
            
    def modify_shell(self, read_data, 
                           param_file,
                           input_script, 
                           shell_script, path):
        """ Modifies the shell found at shell_loc by inserting lines
        required by the potential. 
        
        Parameters
        ----------
        read_data : str
            file containing initial water configurations.
        input_script : str
            the modified script.
        shell_script : str
            file containing LAMMPS input shell.
        path : str
            path to data directory.
        """
        element_string = ""
        masses = []
        for key, value in self.masses.items():
            element_string += key + " "
            masses.append(value)
        
        self.input_script = input_script
        f = open(shell_script, "r")
        contents = f.readlines()
        f.close()
        
        # copy read_data
        from shutil import copyfile
        copyfile(read_data, path + "initial_config.data")
        
        contents.insert(4, "read_data initial_config.data\n")
        contents.insert(5, "pair_style vashishta\n")
        contents.insert(6, "pair_coeff * * {} {}\n".format(param_file, element_string))
        for i in range(len(masses)):
            contents.insert(9+i, "mass" + 12 * " " + str(i+1) + " " + str(masses[i]) + "\n")

        f = open(input_script, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()

    def set_input_script(self, filename):
        head, self.lmp_script = os.path.split(filename)
        copyfile(filename, self.pwd + self.lmp_script)
        
    def __call__(self, var={}):
        """ Run LAMMPS simulation with the parameters. 
        
        Parameters
        ----------
        params : dictionary   
            Nested dictionary with new parameters. Has to be in the form of: 
            {"comb1": {"param1": value1, "param2": value2, ...}, 
             "comb2": {"param1": value1, "param2": value2, ...},
             ...}.
        read_data : str
            file containing initial particle configurations.
        lammps_exec : str
            LAMMPS executable.
        shell_script : str
            file containing LAMMPS input shell.
        path : str
            path to data directory. Both relative and absolute
            paths work.
        input_script : str
            LAMMPS script name. script.in by default.
        param_file : str
            LAMMPS parameter file name. dest.vashishta by default.
        """
        os.main_path = os.getcwd()
        os.chdir(self.pwd)
        self.computer(self.lmp_script, var)
        return None
        
        
if __name__ == "__main__":

    # EXAMPLE USAGE
    from substance import Water
    from computer import CPU, GPU, Slurm_CPU, Slurm_GPU 
    from directory import Custom, Verbose
    from math import cos, pi
    
    # Set parameters
    Z_Hs = [0.50]
    thetas = [95]
    Bs = [0.4]
    Hs = [1.0]
    Ds = [0.1]
    #lambda4s = [1.4, 1.5, 1.6]
    
    # Simulate
    for Z_H in Z_Hs:
      for theta in thetas:
        for B in Bs:
          for H in Hs:
            for D in Ds:
              #for lambda4 in lambda4s:
              Z_O = - 2 * Z_H
              params = {"HHH" : {"Zi" : Z_H, "Zj" : Z_H},
                        "OOO" : {"Zi" : Z_O, "Zj" : Z_O},
                        "HOO" : {"Zi" : Z_H, "Zj" : Z_O, "H" : H, "D" : D},
                        "OHH" : {"Zi" : Z_O, "Zj" : Z_H, "H" : H, "D" : D,  
                                 "cos(theta)" : cos(theta * pi / 180), "B" : B}}
                      
              sim = AutoSim(substance=Water(init_config="watercube_4nm.data"), 
                                            directory=Custom("simulation", overwrite=True),
                                            computer=CPU(num_procs=18))
              sim.generate_parameter_file("H2O.vashishta", params=params)
              sim.set_input_script("script.in")
              sim()
    
    
    
