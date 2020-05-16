""" Simulation interface for LAMMPS using the Vashishta potential.
Prerequisites include a recent version of LAMMPS with the manybody
package built and Python 3.x. For example usage, see bottom.

@author Even Marius Nordhagen
"""

class AutoSim:

    from computer import CPU
    def __init__(self, substance):
        """ Initialize class
        
        Parameters
        ----------
        substance : obj
            which potential to use
        """
        self.substance = substance
        self.parameters, self.masses = substance()
        
                    
    def set_parameters(self, parameters):
        """ This function overwrites the default parameters.
        
        Parameters
        ----------
        parameters : dictionary   
            nested dictionary with new parameters. Has to be in the form of: 
            {"comb1": {"param1": value1, "param2": value2, ...}, 
             "comb2": {"param1": value1, "param2": value2, ...},
             ...}.
        """
        for comb, params in parameters.items():
            for param, value in params.items():
                self.parameters[comb][param] = value
                
    def generate_directory(self, params, inter, header=""):
        """ Generate directory or subdirectory as a string
        based on some parameters.
        
        Parameters
        ----------
        params : dictionary
            dictionary containing the shortings to be used in directory name
            and the actual parameter names. Should be in the form of:
            {"name1":"shorting1", "name2":"shorting2", ...}
        inter : str
            which interaction type we are looking at
        header : str
            what the directory name should start with
        """
        path = ""
        slash = True
        for short, name in params.items():
            if slash:
                path += "/" + header
                slash = False
            else:
                path += "_"
            path += short + str(self.parameters[inter][name])
        return path
                
    def generate_path(self):
        """ Generate path to data.
        """
        # TODO: local and global parameters should be substance methods
        local_params = {"H":"H", "e":"eta", "Lo":"lambda1", "D":"D",
                        "Lf":"lambda4", "W":"W", "rc":"rc", "B":"B", 
                        "g":"gamma", "ro":"r0", "C":"C", "t":"cos(theta)"}
        # Substance name is the main directory
        path = repr(self.substance)
        # Subdirectory should contain information about the global parameters
        global_params = {"ZO":"Zi"}
        path += self.generate_directory(global_params, "OOO")

        # Subsubdirectory should contain information about the local parameters   
        for name, params in self.parameters.items(): 
            path += self.generate_directory(local_params, name, name + "_")
        self.path = path
        return path
        
    def make_tree(self, path):
        """ Make a tree based on some path.
        
        Parameters
        ----------
        path : str
            string with the path
        """
        import os
        try:
            # Create target Directory
            os.makedirs(path)
            #print("Directory ", path, " created")
        except FileExistsError:
            pass
            #print("Directory ", path, " already exists")
        
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
        
        
        
    def generate_parameter_file(self, filename, 
                                      header_filename=".perm/header.vashishta"):
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
        # Add header to file
        from shutil import copyfile
        copyfile(header_filename, filename)
        
        # Add parameters to file
        for name, params in self.parameters.items():
            self.append_type_to_file(name, params, filename)
        
            
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

        
    def __call__(self, params={},
                       computer=CPU(),
                       shell_script=".perm/lammps/shell.in",
                       path="data/",
                       lmps_script="script.in",
                       param_file="dest.vashishta"):
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
        # change desired parameters
        self.set_parameters(params)
        
        # generate path to working dir
        self.data_directory = self.generate_path()
        
        # add global path to working dir
        path += self.data_directory + "/"
        self.path = path
        
        # make working dir
        self.make_tree(path)
        
        # generate file with all parameters to be used by LAMMPS
        self.generate_parameter_file(path + param_file)
    
        # add the correct parameter file and bulk file to shell.in
        self.modify_shell(self.substance.init_config, param_file, path+lmps_script, shell_script, path)
        computer(path, lmps_script)
        return None
        
        
if __name__ == "__main__":

    # EXAMPLE USAGE
    from substances import Water
    from computer import CPU, GPU, Slurm_CPU, Slurm_GPU 
    from math import cos, pi
    
    # Set parameters
    Z_Hs = [0.50]
    thetas = [95, 100, 105]
    Bs = [0.4,0.5,0.6]
    Hs = [1.0]
    Ds = [0.1, 0.3, 0.5]
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
                      
              sim = AutoSim(substance=Water(bulk=".perm/water/water_lmps.data"))
              sim(params=params,
                  computer=GPU(),
                  shell_script=".perm/lammps/shell_10MPa.in",
                  path="data_10MPa/")
    
    
    
