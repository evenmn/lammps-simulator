class Directory:
    def __init__(self):
        self.path = ""
        
        
class Custom(Directory):
    """ Set source directory to custom location.
    
    Parameters
    ----------
    directory : str
        source directory location
    overwrite : bool
        if the specified directory exists, the files will be overwritten by default
    """
    
    def __init__(self, directory, overwrite=True):
        self.directory = directory
        self.overwrite = overwrite
    
    def __call__(self, params):
        import os
        if self.overwrite:
            try:
                os.makedirs(self.directory)
            except:
                pass
            return self.directory
        else:
            import os
            ext = 0
            path = self.directory
            repeat=True
            while repeat:
                try:
                    os.makedirs(path)
                    repeat=False
                except FileExistsError:
                    ext += 1
                    path = self.directory + f"_{ext}"
            return path
    
class Verbose(Directory):
    """ The source directory 
    """
    def __init__(self):
        pass
    
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
            path += short + str(params[inter][name])
        return path
                
    def generate_path(self, params):
        """ Generate path to data.
        """
        # TODO: local and global parameters should be substance methods
        local_params = {"H":"H", "e":"eta", "Lo":"lambda1", "D":"D",
                        "Lf":"lambda4", "W":"W", "rc":"rc", "B":"B", 
                        "g":"gamma", "ro":"r0", "C":"C", "t":"cos(theta)"}
        # Substance name is the main directory
        # Subdirectory should contain information about the global parameters
        global_params = {"ZO":"Zi"}
        path = self.generate_directory(global_params, "OOO")

        # Subsubdirectory should contain information about the local parameters   
        for name, _ in params.items(): 
            path += self.generate_directory(local_params, name, name + "_")
        return path
        
    def __call__(self, params):
        """ Make a tree based on some path.
        
        Parameters
        ----------
        path : str
            string with the path
        """
        self.path = self.generate_path(params)
        import os
        try:
            # Create target Directory
            os.makedirs(self.path)
        except FileExistsError:
            pass
        return self.path
            
class Exdir(Directory):
    def __init__(self):
        pass
        
    def __call__(self):
        pass
