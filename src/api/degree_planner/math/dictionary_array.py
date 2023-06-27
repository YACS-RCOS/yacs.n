from collections import OrderedDict

class Dict_Array():

    def __init__(self, list_type='list', ordered_dict=False):
        if ordered_dict:
            self.dictionary = OrderedDict()
        else:
            self.dictionary = dict()
        self.list_type = list_type


    def convert_list_type(self, list_type):
        for key, elements in self.dictionary.items():
            if list_type == 'list':
                self.dictionary.update({key:list(elements)})
            elif list_type == 'set':
                self.dictionary.update({key:set(elements)})


    def add(self, key, element, overwrite=False) -> None:
        '''
        adds element to dict array by appending it to array of its cooresponding key
        '''
        if key in self.dictionary:
            if self.list_type == 'list':
                if overwrite:
                    self.dictionary.update({key:[element]})
                else:
                    self.dictionary.get(key).append(element)
            elif self.list_type == 'set':
                if overwrite:
                    self.dictionary.update({key:{element}})
                else:
                    self.dictionary.get(key).add(element)
        else:
            if self.list_type == 'list':
                self.dictionary.update({key:[element]})
            elif self.list_type == 'set':
                self.dictionary.update({key:{element}})


    def extend_elements(self, key, elements, overwrite=False) -> None:
        '''
        parameters:
            key: key of elements
            elements: iterable set to append to dictionary

        iterate over elements to add to values of its cooresponding keys in dictionary
        '''
        if key in self.dictionary:
            if overwrite:
                self.dictionary.update({key:elements})
            elif self.list_type == 'list':
                self.dictionary.get(key).extend(elements)
            elif self.list_type == 'set':
                self.dictionary.get(key).update(elements)
        else:
            if self.list_type == 'list':
                self.dictionary.update({key:list(elements)})
            elif self.list_type == 'set':
                self.dictionary.update({key:set(elements)})


    def extend(self, other, overwrite=False):
        '''
        other (Dict_Array)

        merges two dict arrays together
        '''
        for key, elements in other.dictionary.items():
            self.extend_elements(key, elements, overwrite)


    def remove(self, key, element=None, suppress_error=False) -> None:
        try:
            if key not in self.dictionary:
                if suppress_error:
                    return
                raise ValueError("key not found")
            
            if element is None:
                self.dictionary.pop(key)
            
            if self.list_type == 'list':
                self.dictionary.get(key).remove(element)
            elif self.list_type == 'set':
                self.dictionary.get(key).remove(element)
                
        except ValueError as e:
            if suppress_error:
                return
            raise ValueError(e)


    def rename_key(self, old_key, new_key, suppress_error=False):
        if old_key not in self.dictionary:
            if suppress_error:
                return
            raise ValueError('key not found')
        elements = self.dictionary.get(old_key)
        self.dictionary.pop(old_key)
        self.dictionary.update({new_key:elements})


    def pop(self, key) -> list:
        return self.dictionary.pop(key, [])


    def replace(self, key, element) -> None:
        self.remove(key)
        self.add(key, element)


    def contains(self, key, element) -> bool:
        return element in self.dictionary.get(key, [])
    
    
    def to_tuples(self):
        return [[key, elements] for key,elements in self.dictionary.items()]


    def items(self):
        return self.dictionary.items()


    def __len__(self):
        return len(self.dictionary)


    def __repr__(self):
        return str(self.dictionary)
