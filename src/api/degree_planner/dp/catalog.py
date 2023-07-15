from .element import Element
from .template import Template
from ..io.output import Output


class Catalog():

    def __init__(self):

        self.elements = dict()
        self.templates = dict()
        self.tags = dict()

        self.debug = Output(Output.OUT.DEBUG)

    def add(self, items):
        '''add an element or template or an iterable of elements/templates'''
        if hasattr(items, '__iter__'):
            for e in items:
                self.add(e)
            return
        
        if isinstance(items, Element):
            self.elements.update({items.name:items})
        elif isinstance(items, Template):
            self.templates.update({items.name:items})

    def remove(self, items):
        '''remove an element or template or an iterable of elements/templates'''
        if hasattr(items, '__iter__'):
            for e in items:
                self.remove(e)
            return
        
        if isinstance(items, Element):
            self.elements.pop(items.name, None)
        elif isinstance(items, Template):
            self.templates.update(items.name, None)

    def remove_element(self, element_name):
        '''remove element by name'''
        self.elements.pop(element_name, None)

    def remove_template(self, template_name):
        '''remove template by name'''
        self.templates.pop(template_name, None)

    def get_element(self, element_name):
        return self.elements.get(element_name, None)
    
    def get_template(self, template_name):
        return self.templates.get(template_name, None)
    
    def get_elements(self):
        return self.elements.values()
    
    def get_templates(self):
        return self.templates.values()
    
    def __repr__(self):
        count = 1
        printout = f"catalog:"
        for element in self.elements.values():
            printout+=str(count) + ": " + str(element) + "\n"
            count+=1
        count = 1
        for template in self.templates.values():
            printout+=str(count) + ": " + str(template) + "\n"
            count+=1
        return printout
    
    def __str__(self):
        return f"catalog: {len(self.elements)} elements, {len(self.templates)} templates"
