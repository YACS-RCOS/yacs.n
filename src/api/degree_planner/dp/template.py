class Template():

    def __init__(self, name):
        self.name = name
        self.requirements = list()
        self.groups = list()

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
