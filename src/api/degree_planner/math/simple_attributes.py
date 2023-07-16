'''
BUGGY, NEED SOME FIXING
'''

from .dictionary_array import Dict_Array

class Simple_Attributes():

    def __init__(self):
        self.attributes_str = set()
        self.attributes = Dict_Array()
    
    def add_attribute(self, attr:str):
        first_dot = attr.find('.')
        head = attr[:first_dot]
        body = attr[first_dot + 1:]
        self.attributes.add(head, body)
        self.attributes_str.add(attr)
        #print(f'added attribute {attr}, current states: \n {self.attributes}')

    def remove_attribute(self, attr:str):
        first_dot = attr.find('.')
        head = attr[:first_dot]
        body = attr[first_dot + 1:]
        self.attributes.remove(head, body)
        self.attributes_str.remove(attr)
        #print(f'removed attribute {attr}, current states: \n {self.attributes}')

    def get_attributes_by_head(self, attr:str):
        '''
        returns all attributes with that head
        '''
        if attr == '':
            return list(self.attributes_str)
        bodies = self.attributes.get(attr, [])
        attributes = list()
        for body in bodies:
            if body == '':
                attributes.append(f'{attr}')
            else:
                attributes.append(f'{attr}.{body}')
        return attributes
    
    def get_attributes_body_by_head(self, attr:str):
        return self.attributes.get(attr, [])

    def remove_attributes_by_head(self, attr:str):
        for attribute in self.get_attributes_by_head(attr):
            self.remove_attribute(attribute)

    def replace_attribute(self, head:str, body:str):
        if len(self.get_attributes_by_head(head)) > 0:
            self.remove_attributes_by_head(head)
            self.add_attribute(f'{head}.{body}')

    def get_attributes_ge(self, attr):
        bodies = self.attributes.get(head(attr), [])
        bodies_ge = [possibility for possibility in bodies if possibility >= body(attr)]
        print(f"attribute {attr} with head {head(attr)} matched with bodies {bodies} with bodies ge {bodies_ge}")
        return [f"{head(attr)}.{body}" if head(attr) != '' else body for body in bodies_ge]
    
    def get_attributes_le(self, attr):
        bodies = self.attributes.get(head(attr), [])
        bodies_le = [possibility for possibility in bodies if possibility <= body(attr)]
        print(f"attribute {attr} with head {head(attr)} matched with bodies {bodies} with bodies ge {bodies_le}")
        return [f"{head(attr)}.{body}" if head(attr) != '' else body for body in bodies_le]

    def attr(self, attr:str):
        '''
        returns only the body of the attribute specified
        '''
        if '.' in attr:
            bodies = self.attributes.get(head(attr), None)
            if bodies is None:
                return None
            if body(attr) in bodies:
                return []
            return None
        return self.attributes.get(attr, None)

    def __eq__(self, other):
        if not isinstance(other, Simple_Attributes):
            return False
        return self.attributes_str == other.attributes_str
    
    def __iter__(self):
        for attr in self.attributes_str:
            yield attr

    def __len__(self):
        return len(self.attributes_str)
    
    def __str__(self):
        return ', '.join(self.attributes_str)
    
    def __repr__(self):
        return ', '.join(self.attributes_str)
    
    def __hash__(self):
        hash = 0
        for attr in self.attributes_str:
            hash += hash(attr)
        return hash

def head(attr:str) -> str:
    return attr[:attr.find('.')]

def body(attr:str) -> str:
    if '.' not in attr:
        return ''
    return attr[attr.find('.') + 1:]
