import os
import shutil
from re import findall

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
            self.wd = directory
            try:
                os.makedirs(directory)
            except:
                pass
        else:
            ext = 0
            repeat=True
            while repeat:
                try:
                    os.makedirs(self.wd)
                    repeat=False
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

    def ordered_parameter_string(self, params, param_suffices, param_list, string):
        """Returning an ordered list of all the parameter values

        :type params: dict
        :param params: dictionary with all parameters
        :type param_suffices: list of str
        :param param_suffices: list of all parameter suffices (e.g. "Zi") correctly ordered
        :type param_list: list
        :param param_list: initial list to append parameters to
        :type string: str
        :param string: initial string that will be extended with all parameters
        """

        for suffix in param_suffices:
            param_list.append(params[suffix])
        for param in param_list:
            string += str(param) + "  \t"
        return string + "\n"

    def append_type_to_file(self, name, params, filename):
        """Append the actual parameter values to the parameter file.

        :type name: str
        :param name: name of interaction combo (e.g. "SiSiSi")
        :type params: dict
        :param params: dictionary with all parameters
        :type filename: str
        :param filename: parameter filename
        """
        # Split name
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
        """Generates input parameter file for the potential. The default
        parameters are the ones specified in Wang et al., so parameters
        that are not specified will fall back on these default parameters.

        :param substance: substance to simulate
        :type substance: str
        :param filename: filename of parameter file
        :type filename: str
        :param params: dictionary of parameters that should be changed
        :type params: dict
        """
        # Get default parameters
        if substance == "water":
            from .substance import water
            self.params = water
        elif substance == "silica":
            from .substance import silica
            self.params = silica
        else:
            raise NotImplementedError("The currently available substances are 'silica' and 'water'")

        # Merge given parameters with default parameters
        for comb, parameters in params.items():
            combs = comb.split(",")
            for c in combs:
                if c == "global":
                    if substance == "water":
                        for key, value in parameters.items():
                            if key == "Z_O":
                                Z_H = - value / 2
                                self.params["HHH"]["Zi"] = Z_H
                                self.params["HHH"]["Zj"] = Z_H
                                self.params["OOO"]["Zi"] = value
                                self.params["OOO"]["Zj"] = value
                                self.params["HOO"]["Zi"] = Z_H
                                self.params["HOO"]["Zj"] = value
                                self.params["OHH"]["Zi"] = value
                                self.params["OHH"]["Zj"] = Z_H
                            elif key == "Z_H":
                                Z_O = - 2 * value
                                self.params["HHH"]["Zi"] = value
                                self.params["HHH"]["Zj"] = value
                                self.params["OOO"]["Zi"] = Z_O
                                self.params["OOO"]["Zj"] = Z_O
                                self.params["HOO"]["Zi"] = value
                                self.params["HOO"]["Zj"] = Z_O
                                self.params["OHH"]["Zi"] = Z_O
                                self.params["OHH"]["Zj"] = value
                            else:
                                raise NotImplementedError(f"No global parameter {key}")
                    elif substance == "silica":
                        for key, value in parameters.items():
                            if key == "Z_Si":
                                Z_O = - value / 2
                                self.params["SiSiSi"]["Zi"] = value
                                self.params["SiSiSi"]["Zj"] = value
                                self.params["OOO"]["Zi"] = Z_O
                                self.params["OOO"]["Zj"] = Z_O
                                self.params["SiOO"]["Zi"] = value
                                self.params["SiOO"]["Zj"] = Z_O
                                self.params["OSiSi"]["Zi"] = Z_O
                                self.params["OSiSi"]["Zj"] = value
                            elif key == "Z_O":
                                Z_Si = - 2 * value
                                self.params["SiSiSi"]["Zi"] = Z_Si
                                self.params["SiSiSi"]["Zj"] = Z_Si
                                self.params["OOO"]["Zi"] = value
                                self.params["OOO"]["Zj"] = value
                                self.params["SiOO"]["Zi"] = Z_Si
                                self.params["SiOO"]["Zj"] = value
                                self.params["OSiSi"]["Zi"] = value
                                self.params["OSiSi"]["Zj"] = Z_Si
                            else:
                                raise NotImplementedError(f"No global parameter {key}")

                elif c == "all":
                    for key, value in parameters.items():
                        if substance == "water":
                            self.params["HHH"][key] = value
                            self.params["OOO"][key] = value
                            self.params["OHH"][key] = value
                            self.params["HOO"][key] = value
                        elif substance == "silica":
                            self.params["SiSiSi"][key] = value
                            self.params["OOO"][key] = value
                            self.params["SiOO"][key] = value
                            self.params["OSiSi"][key] = value

                else:
                    for parameter, value in parameters.items():
                        self.params[c][parameter] = value

        # Make new parameter file
        this_dir, this_filename = os.path.split(__file__)
        header_filename = this_dir + "/data/header.vashishta"
        self.param_file = filename

        shutil.copyfile(header_filename, self.wd + self.param_file)

        # Add parameters to file
        for name, params in self.params.items():
            self.append_type_to_file(name, params, self.wd + self.param_file)

    def set_lammps_script(self, filename, copy=True, var**):
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

        :param computer: how to run the simulation. Options are 'CPU', 'GPU', 'SlurmCPU' and 'SlurmGPU', see computer.py
        :type computer: obj
        """
        main_path = os.getcwd()
        os.chdir(self.wd)
        computer(self.lmp_script, self.var)
        os.chdir(main_path)
