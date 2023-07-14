class Attributes():

    def __init__(self):
        self.attributes_head_to_body_str = dict()
        self.attributes_full_str_to_list = dict()
    
    def add_attribute(self, attr:str):
        attr = attr.casefold()
        attr_split = attr.split('.')
        self.attributes_full_str_to_list.update({attr:attr_split})
        for i in range(0, len(attr_split) + 1):
            head = '.'.join(attr_split[:i])
            body = '.'.join(attr_split[i:])
            update_dict(self.attributes_head_to_body_str, head, body)
        # print(f'added attribute {attr}, current states: \n full_str: {self.attributes_full_str_to_list}\n head and body: {self.attributes_head_to_body_str}')

    def remove_attribute(self, attr:str):
        attr_split = attr.split('.')
        if self.attributes_full_str_to_list.pop(attr, None) is None:
            return
        for i in range(0, len(attr_split) + 1):
            head = '.'.join(attr_split[:i])
            body = '.'.join(attr_split[i:])
            update_dict(self.attributes_head_to_body_str, head, body, True)
        # print(f'removed attribute {attr}, current states: \n full_str: {self.attributes_full_str_to_list}\n head and body: {self.attributes_head_to_body_str}')

    def get_attributes_by_head(self, attr:str):
        '''
        returns all attributes with that head
        '''
        if attr == '':
            return self.attributes_full_str_to_list.keys()
        bodies = self.attributes_head_to_body_str.get(attr, {})
        attributes = list()
        for body in bodies:
            if body == '':
                attributes.append(f'{attr}')
            else:
                attributes.append(f'{attr}.{body}')
        return attributes
    
    def get_attributes_body_by_head(self, attr:str):
        bodies = self.attributes_head_to_body_str.get(attr, {})
        return list(bodies)

    def remove_attributes_by_head(self, attr:str):
        for attribute in self.get_attributes_by_head(attr):
            self.remove_attribute(attribute)

    def replace_attribute(self, head:str, body:str):
        if len(self.get_attributes_by_head(head)) > 0:
            self.remove_attributes_by_head(head)
            self.add_attribute(f'{head}.{body}')

    def get_attributes_ge(self, attr):
        bodies_of_head_matches = self.get_attributes_body_by_head(no_tail(attr))
        bodies_ge = [possibility for possibility in bodies_of_head_matches if possibility >= tail(attr)]
        # print(f"attribute {attr} with no tail {no_tail(attr)} matched with bodies {bodies_of_head_matches} with bodies ge {bodies_ge}")
        return [f"{no_tail(attr)}.{body}" if no_tail(attr) != '' else body for body in bodies_ge]
    
    def get_attributes_le(self, attr):
        bodies_of_head_matches = self.get_attributes_body_by_head(no_tail(attr))
        bodies_le = [possibility for possibility in bodies_of_head_matches if possibility <= tail(attr)]
        # print(f"attribute {attr} with no tail {no_tail(attr)} matched with bodies {bodies_of_head_matches} with bodies ge {bodies_ge}")
        return [f"{no_tail(attr)}.{body}" if no_tail(attr) != '' else body for body in bodies_le]

    def attr(self, head:str):
        '''
        returns only the body of the attribute specified
        '''
        bodies = self.attributes_head_to_body_str.get(head, None)
        # print(f'get attribute with head {head}, current states: \n full_str: {self.attributes_full_str_to_list}\n head and body: {self.attributes_head_to_body_str}\n found {bodies}')
        if bodies is None:
            return None
        if len(bodies) == 1:
            for body in bodies:
                return body
        return bodies
    
    def next_attr(self, head:str):
        next_values = list()
        for body in self.attributes_head_to_body_str.get(head):
            if len(body):
                next_values.append(body[:body.find('.')])
        return next_values

    def __eq__(self, other):
        if not isinstance(other, Attributes):
            return False
        for head in self.attributes_full_str_to_list.keys():
            if head not in other.attributes_full_str_to_list:
                return False
        return True
    
    def __iter__(self):
        for attr in self.attributes_full_str_to_list.keys():
            yield attr

    def __len__(self):
        return len(self.attributes_full_str_to_list)
    
    def __str__(self):
        return ', '.join(self.attributes_full_str_to_list.keys())
    
    def __repr__(self):
        return ', '.join(self.attributes_full_str_to_list.keys())
    
    def __hash__(self):
        hash = 0
        for attr in self.attributes_full_str_to_list.keys():
            hash += hash(attr)
        return hash


def head(attr) -> str:
    return attr[:attr.find('.')]

def body(attr) -> str:
    if '.' not in attr:
        return ''
    return attr[attr.find('.') + 1:]

def tail(attr) -> str:
    return attr[attr.rfind('.') + 1:]

def no_tail(attr) -> str:
    if '.' not in attr:
        return ''
    return attr[:attr.rfind('.')]

def update_dict(dictionary:dict, key, value, remove=False):
    if remove:
        dictionary.get(key).discard(value)
        if not len(dictionary.get(key)):
            dictionary.pop(key)
        return

    if key in dictionary:
        dictionary.get(key).add(value)
    else:
        dictionary.update({key:{value}})
