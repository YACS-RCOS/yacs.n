from ..recommender.recommender import Recommender
from .element import Element
from .template import Template
from ..math.search import Search
from ..io.output import Output


class Catalog():

    def __init__(self, enable_tensorflow=True):

        self.elements = dict()
        self.templates = dict()

        self.tags = dict()
        self.recommender = Recommender(self, enable_tensorflow=enable_tensorflow)

        self.element_searcher = Search()
        self.template_searcher = Search()

        self.debug = Output(Output.OUT.DEBUG)

    def reindex(self, recompute_cache=True):
        '''
        1) computes search index
        2) recaches recommender if tensorflow is enabled
        '''
        self.debug.info('starting search indexing')
        self.element_searcher.update_items(self.elements.keys())
        self.element_searcher.generate_index()

        self.template_searcher.update_items(self.templates.keys())
        self.template_searcher.generate_index()
        self.debug.info('finished search indexing')

        if recompute_cache:
            self.debug.info('starting recommender reindex')
            self.recommender.recache()
            self.debug.info('finished recommender reindex')

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
        '''will use search function to find unique element based on name. If multiple matches, return None'''
        full_name = self.search_element(element_name)
        if len(full_name) != 1:
            return None
        return self.elements.get(full_name[0], None)
    
    def get_template(self, template_name):
        '''will use search function to find unique template based on name. If multiple matches, return None'''
        full_name = self.search_template(template_name)
        if len(full_name) != 1:
            return None
        return self.templates.get(full_name[0], None)
    
    def search_element(self, element_name):
        return self.element_searcher.search(element_name.casefold())
    
    def search_template(self, template_name):
        return self.template_searcher.search(template_name.casefold())
    
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
