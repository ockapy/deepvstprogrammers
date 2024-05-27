import random
import numpy

  
class PluginPatch:
    
    def __init__(self):
        self.parameters_names = []
        self.patch = {}
        self.forbidden_parameters = {}
            
    def set_parameters_name(self,description):
        names_arr = description.split("\n")
        for value in names_arr:
            result = value.split(":")
            if len(result) > 1:
                self.parameters_names.append(result[1])
    
    def initiate_patch(self,data,override_list):
        self.patch = {x: y for x, y in data}
        self.forbidden_parameters = {x: y for x, y in override_list}
            
    def set_forbidden_parameters(self,override_list):
        self.forbidden_parameters = {x: y for x, y in override_list}
    
    def randomise(self):
        for x in self.patch:
            self.patch[x] = random.random()

    def override_parameters(self):
        for x in self.forbidden_parameters.keys():
            self.patch[x] = self.forbidden_parameters[x]
            
    def to_list(self):
        return list(self.patch.items())
    
    def set_patch(self,patch: tuple):
        self.patch = {x:y for x,y in patch}
        
    def update_values(self,patch: list):
        for key, new_value in zip(self.patch.keys(), patch):
            self.patch[key] = new_value
    
    def get_parameters(self):
        parameters = []
        for tuple in self.patch:
            parameters.append(tuple[1])
        return numpy.asarray(parameters,dtype=numpy.float32)

