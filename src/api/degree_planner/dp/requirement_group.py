class Requirement_Group():

    def __init__(self, name, minimum_requirements:dict=None, requirements:list=None, separate_fulfillment=False):
        self.name = name
        self.minimum_requirements = minimum_requirements
        self.separate_fulfillment = separate_fulfillment
        self.requirements = requirements

    def get_requirement_names(self):
        return [requirement.name for requirement in self.requirements]
    
    def __str__(self):
        return f"requirement group {self.name} with requirements {self.get_requirement_names()}"
    
    def __len__(self):
        return len(self.requirements)
    
    def __eq__(self, other):
        if not isinstance(other, Requirement_Group):
            return False
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)