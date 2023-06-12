'''
Fulfillment_Status class
'''

import json
from .course import Course


class Fulfillment_Status():
    '''
    A data structure to store information on fulfillment status of a template
    '''

    def __init__(self, template, required_count:int=0, fulfillment_set:set=None):
        if fulfillment_set == None: fulfillment_set = set()
        self.template = template
        self.required = required_count
        self.fulfillment_set = fulfillment_set

    def fulfilled(self):
        return self.get_actual_count() - self.get_required_count() >= 0

    def get_required_count(self) -> int:
        return self.required
    
    def set_required_count(self, requires) -> None:
        self.required = requires

    def get_actual_count(self) -> int:
        return len(self.fulfillment_set)
    
    def get_fulfillment_set(self) -> set:
        return self.fulfillment_set
    
    def set_fulfillment_set(self, fulfillment_set:set) -> None:
        self.fulfillment_set = fulfillment_set

    def set_template(self, template) -> None:
        self.template = template

    def get_template(self):
        return self.template

    """
    returns whether the element is added (not previously present)
    """
    def add_fulfillment_course(self, course) -> bool:
        len_original = len(self.fulfillment_set)
        if hasattr(course, '__iter__'):
            self.fulfillment_set.update(course)
            return
        self.fulfillment_set.add(course)
        return len_original != len(self.fulfillment_set)

    """
    returns whether the element requested to be removed is present (successful removal)
    """
    def remove_fulfillment_course(self, course:Course) -> bool:
        len_original = len(self.fulfillment_set)
        self.fulfillment_set.discard(course)
        return len_original != len(self.fulfillment_set)

    def unfulfilled_count(self) -> int:
        return max(0, self.get_required_count() - self.get_actual_count())
    
    def excess_count(self) -> int:
        return max(0, self.get_actual_count() - self.get_required_count())
    
    def json(self, as_dict=False) -> json:
        '''
        Return this class as a json file
        '''
        stat = dict()
        stat.update({'template':self.template})
        stat.update({'required count':self.get_required_count()})
        stat.update({'fulfillment set':self.get_fulfillment_set()})
        if as_dict:
            return stat
        return json.dumps(stat)
    
    def __repr__(self) -> str:
        return f"template {self.template.name} specifications: {self.template.specifications}  required count: {self.required}  fulfillment set: {[str(e) for e in self.fulfillment_set]}"
    
    def __str__(self):
        return f"{self.template.name} fulfillment set: {[str(e) for e in self.fulfillment_set]}"
    
    def __eq__(self, other):
        return self.template == other.template and self.required == other.required
    
    def __gt__(self, other):
        return self.template.importance < other.template.importance
    
    def __lt__(self, other):
        return self.template.importance > other.template.importance
    
    def __ge__(self, other):
        return self.template.importance <= other.template.importance
    
    def __le__(self, other):
        return self.template.importance >= other.template.importance
    
    def __len__(self):
        return self.get_actual_count()
    
    def __hash__(self):
        return hash(self.template) + self.required + 10
