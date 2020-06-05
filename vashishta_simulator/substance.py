class Substance:
    """ Returns the set of parameter given a substance. 
    Possible substances are Silica, Water and SilicaWater.
    """
    def __init__(self, init_config):
        self.init_config = init_config
        raise NotImplementedError("The substance {} has no default parameters."
                                  .format(self.__class__))
        
    def __call__(self):
        raise NotImplementedError("Class {} has no instance '__call__'."
                                  .format(self.__class__.__name__))
                                  
class Custom(Substance):
    def __init__(self, init_config, masses, params):
        self.init_config=init_config
        self.masses=masses
        self.params=params
        
    def __repr__(self):
        return "custom"
        
    def __str__(self):
        return "Custom"
        
    def __call__(self):
        return params, masses
        
class Silica(Substance):
    """Default parameters taken from Vashishta 1990.
    """
    def __init__(self, init_config,
                       mass_Si=28.0855, 
                       mass_O=15.9994):
        self.init_config=init_config
        self.mass_Si=mass_Si
        self.mass_O=mass_O
        
    def __repr__(self):
        return "silica"
        
    def __str__(self):
        return "Silica"
        
    def __call__(self):
        SiSiSi = {"H" : 0.39246, 
                  "eta" : 11, 
                  "Zi" : 1.2, 
                  "Zj" : 1.2, 
                  "lambda1" : 4.43, 
                  "D" : 0.0, 
                  "lambda4" : 2.5, 
                  "W" : 0.0, 
                  "rc" : 5.5, 
                  "B" : 0.0, 
                  "gamma" : 0.0, 
                  "r0" : 0.0, 
                  "C" : 0.0, 
                  "cos(theta)" : 0.0}
    
        OOO = {"H" : 355.5263, 
               "eta" : 7, 
               "Zi" : -0.6, 
               "Zj" : -0.6, 
               "lambda1" : 4.43, 
               "D" : 12.4413912, 
               "lambda4" : 2.5, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0" : 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        OSiSi = {"H" : 78.3143, 
                 "eta" : 9, 
                 "Zi" : -0.6, 
                 "Zj" : 1.2, 
                 "lambda1" : 4.43, 
                 "D" : 24.8827823, 
                 "lambda4" : 2.5, 
                 "W" : 0.0, 
                 "rc" : 5.5, 
                 "B" : 19.972, 
                 "gamma" : 1.0, 
                 "r0": 2.60, 
                 "C" : 0.0, 
                 "cos(theta)" : -0.777145961}
    
        SiOO = {"H" : 78.3143, 
                 "eta" : 9, 
                 "Zi" : -0.6, 
                 "Zj" : 1.2, 
                 "lambda1" : 4.43, 
                 "D" : 24.8827823, 
                 "lambda4" : 2.5, 
                 "W" : 0.0, 
                 "rc" : 5.5, 
                 "B" : 4.993, 
                 "gamma" : 1.0, 
                 "r0": 2.60, 
                 "C" : 0.0, 
                 "cos(theta)" : -0.333313248}
    
        SiOSi = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0, 
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 0.0}
    
        SiSiO = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0, 
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 0.0}
    
        OSiO = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
    
        OOSi = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
    
        parameters = {"SiSiSi" : SiSiSi, 
                      "OOO" : OOO, 
                      "OSiSi" : OSiSi, 
                      "SiOO" : SiOO, 
                      "SiOSi" : SiOSi, 
                      "SiSiO" : SiSiO, 
                      "OSiO" : OSiO, 
                      "OOSi" : OOSi}
        masses = {"Si" : self.mass_Si, "O" : self.mass_O}
        return parameters, masses
        
class Water(Substance):
    '''
    Default parameters taken from Wang et al.
    '''
    def __init__(self, init_config,
                       mass_H=1.0079, 
                       mass_O=15.9994):
        self.init_config=init_config
        self.mass_H=mass_H
        self.mass_O=mass_O
        
    def __repr__(self):
        return "water"
        
    def __str__(self):
        return "Water"
    
    def __call__(self):
        HHH = {"H" : 0.0, 
               "eta" : 9, 
               "Zi" : 0.32983, 
               "Zj" : 0.32983, 
               "lambda1" : 4.43, 
               "D" : 0.0, 
               "lambda4" : 2.5, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0" : 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        OOO = {"H" : 1965.88, 
               "eta" : 9, 
               "Zi" : -0.65966, 
               "Zj" : -0.65966, 
               "lambda1" : 4.43, 
               "D" : 2.0887, 
               "lambda4" : 2.5, 
               "W" : 10.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0" : 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        OHH = {"H" : 0.61437, 
               "eta" : 9, 
               "Zi" : -0.65966, 
               "Zj" : 0.32983, 
               "lambda1" : 4.43,   
               "D" : 0.2611, 
               "lambda4" : 1.51113, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 52.9333, 
               "gamma" : 0.75, 
               "r0": 1.4, 
               "C" : 0.0, 
               "cos(theta)" : -0.138267391}
    
        HOO = {"H" : 0.61437, 
               "eta" : 9, 
               "Zi" : 0.32983, 
               "Zj" : -0.65966, 
               "lambda1" : 4.43,   
               "D" : 0.2611, 
               "lambda4" : 1.51113, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        HOH = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0,   
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        HHO = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0,   
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        OHO = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0,   
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        OOH = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0,   
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        parameters = {"HHH" : HHH, 
                      "OOO" : OOO, 
                      "OHH" : OHH, 
                      "HOO" : HOO, 
                      "HOH" : HOH, 
                      "HHO" : HHO, 
                      "OHO" : OHO, 
                      "OOH" : OOH}
        masses = {"H" : self.mass_H, "O" : self.mass_O}
        return parameters, masses
        
class SilicaWater(Substance):
    '''
    Default parameters taken from Wang et al.
    '''
    def __init__(self, init_config,
                       mass_Si=28.0855, 
                       mass_O=15.9994, 
                       mass_H=1.0079):
        self.init_config = init_config
        self.mass_Si=mass_Si
        self.mass_O=mass_O
        self.mass_H=mass_H
        
    def __repr__(self):
        return "silicawater"
        
    def __str__(self):
        return "Silica and water"
        
    def __call__(self):
        SiSiSi = {"H" : 0.39246, 
                  "eta" : 11, 
                  "Zi" : 1.2, 
                  "Zj" : 1.2, 
                  "lambda1" : 4.43, 
                  "D" : 0.0, 
                  "lambda4" : 2.5, 
                  "W" : 0.0, 
                  "rc" : 5.5, 
                  "B" : 0.0, 
                  "gamma" : 0.0, 
                  "r0" : 0.0, 
                  "C" : 0.0, 
                  "cos(theta)" : 0.0}
    
        OOO = {"H" : 355.5263, 
               "eta" : 7, 
               "Zi" : -0.6, 
               "Zj" : -0.6, 
               "lambda1" : 4.43, 
               "D" : 12.4413912, 
               "lambda4" : 2.5, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0" : 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        OSiSi = {"H" : 78.3143, 
                 "eta" : 9, 
                 "Zi" : -0.6, 
                 "Zj" : 1.2, 
                 "lambda1" : 4.43, 
                 "D" : 24.8827823, 
                 "lambda4" : 2.5, 
                 "W" : 0.0, 
                 "rc" : 5.5, 
                 "B" : 19.972, 
                 "gamma" : 1.0, 
                 "r0": 2.60, 
                 "C" : 0.0, 
                 "cos(theta)" : -0.77714596}
    
        SiOO = {"H" : 78.3143, 
                "eta" : 9, 
                "Zi" : 1.2, 
                "Zj" : -0.6, 
                "lambda1" : 4.43, 
                "D" : 24.8827823, 
                "lambda4" : 2.5, 
                "W" : 0.0, 
                "rc" : 5.5, 
                "B" : 4.993, 
                "gamma" : 1.0, 
                "r0": 2.60, 
                "C" : 0.0, 
                "cos(theta)" : -0.333313248}
    
        SiOSi = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0, 
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 0.0}
    
        SiSiO = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0, 
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 0.0}
    
        OSiO = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
    
        OOSi = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
        
        HHH = {"H" : 0.0, 
               "eta" : 9, 
               "Zi" : 0.32983, 
               "Zj" : 0.32983, 
               "lambda1" : 4.43, 
               "D" : 0.0, 
               "lambda4" : 2.5, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0" : 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 1.0}
    
        OOO = {"H" : 1965.88, 
               "eta" : 9, 
               "Zi" : -0.65966, 
               "Zj" : -0.65966, 
               "lambda1" : 4.43, 
               "D" : 2.0887, 
               "lambda4" : 2.5, 
               "W" : 10.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0" : 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 1.0}
    
        OHH = {"H" : 0.61437, 
               "eta" : 9, 
               "Zi" : -0.65966, 
               "Zj" : 0.32983, 
               "lambda1" : 4.43,   
               "D" : 0.2611, 
               "lambda4" : 1.51113, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 52.9333, 
               "gamma" : 0.75, 
               "r0": 1.4, 
               "C" : 0.0, 
               "cos(theta)" : -0.138267391}
    
        HOO = {"H" : 0.61437, 
               "eta" : 9, 
               "Zi" : 0.32983, 
               "Zj" : -0.65966, 
               "lambda1" : 4.43,   
               "D" : 0.2611, 
               "lambda4" : 1.51113, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 1.0}
    
        HOH = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0,   
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 1.0}
    
        HHO = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0,   
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 1.0}
    
        OHO = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0,   
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 1.0}
    
        OOH = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0,   
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 1.0}
               
        HSiSi = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0,   
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 1.0}
                 
        SiHH = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0,   
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 1.0}
                
        SiSiH = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0,   
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 1.0}
                 
        SiHSi = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0,   
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 1.0}
                 
        HSiH = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0,   
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 1.0}
                
        HHSi = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0,   
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 1.0}
                
        OSiH = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0,   
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 1.0}
                
        OHSi = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0,   
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 1.0}
                
        SiOH = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0,   
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 1.0}
                
        SiHO = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0,   
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 1.0}
                
        HSiO = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0,   
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 1.0}
                
        HOSi = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0,   
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 1.0}
    
        parameters = {"SiSiSi" : SiSiSi, 
                      "OOO" : OOO, 
                      "OSiSi" : OSiSi, 
                      "SiOO" : SiOO, 
                      "SiOSi" : SiOSi, 
                      "SiSiO" : SiSiO, 
                      "OSiO" : OSiO, 
                      "OOSi" : OOSi,
                      "HHH" : HHH, 
                      "OOO" : OOO, 
                      "OHH" : OHH, 
                      "HOO" : HOO, 
                      "HOH" : HOH, 
                      "HHO" : HHO, 
                      "OHO" : OHO, 
                      "OOH" : OOH,
                      "HSiSi" : HSiSi,
                      "SiHH" : SiHH,
                      "SiHSi" : SiHSi,
                      "HSiH" : HSiH,
                      "HHSi" : HHSi,
                      "OSiH" : OSiH,
                      "OHSi" : OHSi,
                      "SiOH" : SiOH,
                      "SiHO" : SiHO,
                      "HSiO" : HSiO,
                      "HOSi" : HOSi}
        masses = {"Si" : self.mass_Si, "H" : self.mass_H, "O" : self.mass_O}
        return parameters, masses
        
class SilicaCarbon(Substance):
    """Default parameters.
    """
    def __init__(self, init_config,
                       mass_C=12.0107,
                       mass_Si=28.0855, 
                       mass_O=15.9994):
        self.init_config = init_config
        self.mass_C=mass_C
        self.mass_Si=mass_Si
        self.mass_O=mass_O
        
    def __repr__(self):
        return "silicacarbon"
        
    def __str__(self):
        return "SilicaCarbon"
        
    def __call__(self):
        SiSiSi = {"H" : 0.15500, 
                  "eta" : 11, 
                  "Zi" : 0.7872, 
                  "Zj" : 0.7872, 
                  "lambda1" : 4.43, 
                  "D" : 0.0, 
                  "lambda4" : 2.5, 
                  "W" : 0.0, 
                  "rc" : 5.5, 
                  "B" : 0.0, 
                  "gamma" : 0.0, 
                  "r0" : 0.0, 
                  "C" : 0.0, 
                  "cos(theta)" : 0.0}
    
        OOO = {"H" : 140.38, 
               "eta" : 7, 
               "Zi" : -0.3936, 
               "Zj" : -0.3936, 
               "lambda1" : 4.43, 
               "D" : 5.3504, 
               "lambda4" : 2.5, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0" : 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
    
        OSiSi = {"H" : 30.923, 
                 "eta" : 9, 
                 "Zi" : -0.3936, 
                 "Zj" : 0.7872, 
                 "lambda1" : 4.43, 
                 "D" : 10.701, 
                 "lambda4" : 2.5, 
                 "W" : 0.0, 
                 "rc" : 5.5, 
                 "B" : 19.972, 
                 "gamma" : 1.0, 
                 "r0": 2.60, 
                 "C" : 0.0, 
                 "cos(theta)" : -0.80593}
    
        SiOO = {"H" : 30.923, 
                "eta" : 9, 
                "Zi" : 0.7872, 
                "Zj" : -0.3936, 
                "lambda1" : 4.43, 
                "D" : 10.701, 
                "lambda4" : 2.5, 
                "W" : 0.0, 
                "rc" : 5.5, 
                "B" : 4.993, 
                "gamma" : 1.0, 
                "r0": 2.60, 
                "C" : 0.0, 
                "cos(theta)" : -0.33333333333333333}
    
        SiOSi = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0, 
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 0.0}
    
        SiSiO = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0, 
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 0.0}
    
        OSiO = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
    
        OOSi = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
                
        CCC = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0, 
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
               
        OCC = {"H" : 447.09026, 
               "eta" : 9, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0, 
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 5.5, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
               
        COO = {"H" : 447.09026, 
               "eta" : 9, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0, 
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 5.5,                 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
               
        COC = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0, 
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
                
        CCO = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0, 
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
               
        OCO = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0, 
               "D" : 0.0, 
               "lambda4" : 0.0, 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
                
        OOC = {"H" : 0.0, 
               "eta" : 0.0, 
               "Zi" : 0.0, 
               "Zj" : 0.0, 
               "lambda1" : 0.0, 
               "D" : 0.0, 
               "lambda4" : 0.0,                 
               "W" : 0.0, 
               "rc" : 0.0, 
               "B" : 0.0, 
               "gamma" : 0.0, 
               "r0": 0.0, 
               "C" : 0.0, 
               "cos(theta)" : 0.0}
               
        CSiSi = {"H" : 447.09026, 
                 "eta" : 9, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                  "lambda1" : 0.0, 
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 5.5, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 0.0}
               
        SiCC = {"H" : 447.09026, 
                "eta" : 9, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 5.5, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
               
        SiCSi = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                 "lambda1" : 0.0, 
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 0.0}
                 
        CSiC = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
                
        CCSi = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0, 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
                
        SiSiC = {"H" : 0.0, 
                 "eta" : 0.0, 
                 "Zi" : 0.0, 
                 "Zj" : 0.0, 
                  "lambda1" : 0.0, 
                 "D" : 0.0, 
                 "lambda4" : 0.0, 
                 "W" : 0.0, 
                 "rc" : 0.0, 
                 "B" : 0.0, 
                 "gamma" : 0.0, 
                 "r0": 0.0, 
                 "C" : 0.0, 
                 "cos(theta)" : 0.0}
               
        COSi = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0,                 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
                
        CSiO = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0,                 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
                
        OCSi = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0,                 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
                
        OSiC = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0,                 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
                
        SiOC = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0,                 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
                
        SiCO = {"H" : 0.0, 
                "eta" : 0.0, 
                "Zi" : 0.0, 
                "Zj" : 0.0, 
                "lambda1" : 0.0, 
                "D" : 0.0, 
                "lambda4" : 0.0, 
                "W" : 0.0, 
                "rc" : 0.0,                 
                "B" : 0.0, 
                "gamma" : 0.0, 
                "r0": 0.0, 
                "C" : 0.0, 
                "cos(theta)" : 0.0}
    
        parameters = {"SiSiSi" : SiSiSi, 
                      "OOO" : OOO, 
                      "OSiSi" : OSiSi, 
                      "SiOO" : SiOO, 
                      "SiOSi" : SiOSi, 
                      "SiSiO" : SiSiO, 
                      "OSiO" : OSiO, 
                      "OOSi" : OOSi,
                      "CCC" : CCC,
                      "COC" : COC,
                      "OCO" : OCO,
                      "SiCSi" : SiCSi,
                      "CSiC" : CSiC,
                      "SiCC" : SiCC,
                      "CCSi" : CCSi,
                      "SiSiC" : SiSiC,
                      "CSiSi" : CSiSi,
                      "OCC" : OCC,
                      "CCO" : CCO,
                      "OOC" : OOC,
                      "COO" : COO,
                      "COSi" : COSi,
                      "CSiO" : CSiO,
                      "OCSi" : OCSi,
                      "OSiC" : OSiC,
                      "SiOC" : SiOC,
                      "SiCO" : SiCO}
        masses = {"C" : self.mass_C, "Si" : self.mass_Si, "O" : self.mass_O}
        return parameters, masses
