'''
Course class
'''

import json
from ..math.attributes import Attributes

class Course():
    '''
    Course object containing a dictionary of attributes that uniquely defines the course
    and can be used to search/filter for it

    It also has attributes for fast access which should remain consistent with the attribute
    dictionary
    '''

    def __init__(self, name, subject, course_id):
        # main attributes
        self.unique_name = name
        self.name = name
        self.subject = subject
        self.course_id = course_id

        self.attributes = Attributes()
        self.keywords = list()

        if name not in ('', 'NA', 'ANY'):
            self.set_name(name)
        if subject not in ('', 'NA', 'ANY'):
            self.set_subject(subject)
        if course_id not in (0, -1, '', 'NA', 'ANY'):
            self.set_id(course_id)
            if len(str(course_id)):
                self.set_level(str(course_id)[0])

        self.generate_unique_name()

        self.description = "" # text to be displayed describing the class


    """
    Getters
    """

    def get_name(self):
        return self.name

    def get_unique_name(self):
        return self.unique_name

    def get_subject(self):
        return self.subject

    def get_id(self):
        return self.course_id

    # determines the level of the course, 1000=1, 2000=2, 4000=4, etc
    def get_level(self):
        return self.attr('level')

    def get_credits(self):
        return self.attr('credits')

    def get_crosslisted(self):
        return self.attr('cross_listed', True)


    """
    Setters
    """

    def set_name(self, name):
        self.name = name
        self.replace_attribute('name', name)

    def generate_unique_name(self):
        if self.name == "" or self.get_subject() is None or self.get_id() is None:
            self.unique_name = self.name
        else:
            self.unique_name = f"{self.get_subject().casefold()} {str(self.get_id()).casefold()} {self.get_name().strip().casefold()}"
            self.unique_name = self.unique_name.replace(',', '')
        self.remove_attribute_by_head('unique_name')
        self.add_attribute(f'unique_name.{self.unique_name}')

    def set_subject(self, subject):
        self.subject = subject
        self.remove_attribute_by_head('subject')
        self.add_attribute(f'subject.{subject}')

    def set_id(self, course_id):
        self.course_id = course_id
        self.remove_attribute_by_head('course_id')
        self.add_attribute(f'course_id.{course_id}')
        self.remove_attribute_by_head('level')
        self.add_attribute(f'level.{str(course_id)[0]}')

    def set_credits(self, course_credits):
        self.remove_attribute_by_head('credits')
        self.add_attribute(f'credits.{course_credits}')

    def set_level(self, level):
        self.remove_attribute_by_head('level')
        self.add_attribute(f'level.{level}')


    """
    Attributes are expressed as elements joined by periods,
    but are internally stored in this class as a list
    """

    def add_attribute(self, attr:str) -> None:
        self.attributes.add_attribute(attr)

    def replace_attribute(self, head, body) -> None:
        '''
        removes all attributes with the given head, and replaces it with the provided attribute
        '''
        self.attributes.replace_attribute(head, body)

    def remove_attribute(self, attr) -> None:
        '''
        removes attribute with exact match
        '''
        self.attributes.remove_attribute(attr)

    def attr(self, attr:str, make_list=False) -> str:
        '''
        finds attribute match within self and returns the value
        '''
        attributes = self.attributes.attr(attr)
        if attributes is None or not make_list or hasattr(attributes, '__iter__'):
            return attributes
        return [attributes]

    def get_attributes_by_head(self, attr) -> list:
        return self.attributes.get_attributes_by_head(attr)

    def remove_attribute_by_head(self, attr) -> int:
        '''
        removes all attributes matching the provided head
        '''
        self.attributes.remove_attributes_by_head(attr)

    def get_next(self, head) -> set:
        return self.attributes.next_attr(head)
    
    def get_attributes_ge(self, attr) -> list:
        return self.attributes.get_attributes_ge(attr)

    def get_attributes_le(self, attr) -> list:
        return self.attributes.get_attributes_le(attr)

    def json(self):
        '''
        Returns:
            course (OrderedDict): all course attributes within an ordered dictionary
                includes name, id, id2, major, credits, CI, HASS_inquiry, crosslisted,
                concentrations, pathways, presequisites, restricted, description.

                Some attributes will be omitted if empty, includes all attributes that
                are the form of a list or set.
        '''
        return json.dumps(list(self.attributes))

    def __repr__(self):
        string = (f"{self.unique_name}:\n{self.get_credits()} credits\n" + \
            f"crosslisted with: {self.get_crosslisted()}\n" + \
            f"attributes: {self.attributes}" if len(self.attributes) > 0 else '' + '\n')
        return string.replace("set()", "none")

    def __str__(self):
        return f"{self.subject} {self.course_id} {self.name}"

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        if (self.unique_name == other.unique_name):
            return True
        return False

    def __add__(self, other):
        course = Course('ANY', 'ANY', 'ANY')
        for attr in self.attributes:
            course.add_attribute(attr)
        for attr in other.attributes:
            course.add_attribute(attr)
        course.description = self.description + '\n\n' + other.description
        return course

    def __hash__(self):
        return hash(self.unique_name)
