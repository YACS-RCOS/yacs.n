from ..math.attributes import Attributes

class Template():

    def __init__(self, name):
        self.name = name
        self.requirements = list()
        self.groups = list()
        self.attributes = Attributes(False)

    def compile_attributes(self):
        attributes = Attributes(False)
        for attr in self.attributes.attributes_full_str_to_list.keys():
            attributes.add_attribute(f"{attr}")
        return attributes

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"template {self.name} with requirements {[str(e) for e in self.requirements]}"
    
    def __eq__(self, other):
        if not isinstance(other, Template):
            return False
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
