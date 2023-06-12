'''
Catalog class
'''

import json

from .course import Course
from .degree import Degree
from ..math.search import Search
from ..recommender.recommender import Recommender
from ..io.output import Output

class Catalog():
    '''
    A list of courses and degreees, one catalog should be generated for every planner

    Contains functions to find course match based on a template course and pool of courses
    to search from
    '''

    def __init__(self, enable_tensorflow=True):
        '''
        catalog stores a list of courses, degrees, tags for the recommendation system,
        a recommender object and a search object
        '''
        self.__course_list = dict() # course name as key
        self.__degree_list = dict() # degree name as key

        self.tags = dict() # { subject : [tags] }
        self.recommender = Recommender(self, enable_tensorflow=enable_tensorflow)
        self.searcher = Search()
        self.debug = Output(Output.OUT.DEBUG)

    def reindex(self, recompute_cache=True):
        '''
        1) computes search index
        2) recaches recommender if tensorflow is enabled
        '''
        self.debug.info('starting search indexing')
        self.searcher.update_items(self.course_names())
        self.searcher.generate_index()
        self.debug.info('finished search indexing')

        if recompute_cache:
            self.debug.info('starting recommender reindex')
            self.recommender.recache()
            self.debug.info('finished recommender reindex')

    def add_course(self, courses):
        '''
        may take a list of courses or a single course object
        '''
        if hasattr(courses, '__iter__'):
            for course in courses:
                self.add_course(course)
            return
        self.__course_list.update({courses.unique_name:courses})

    def remove_course(self, courses):
        '''
        may take a list of courses or a single course object/name
        '''
        if hasattr(courses, '__iter__'):
            for course in courses:
                self.remove_course(course)
            return
        if isinstance(courses, str):
            self.__course_list.pop(courses, None)
        else:
            self.__course_list.pop(courses.unique_name, None)

    def add_degree(self, degree:Degree):
        '''
        adds degree to catalog
        '''
        self.__degree_list.update({degree.name:degree})

    def remove_degree(self, degree):
        '''
        removes degree from catalog
        '''
        if isinstance(degree, str):
            self.__degree_list.pop(degree, None)
        else:
            self.__degree_list.pop(degree.name, None)

    def get_course(self, unique_name:str) -> Course:
        '''
        Parameters:
            course_name (str): name of course to get. Must be a unique name

        Returns:
            course (Course): course if found, otherwise None
        '''
        name = self.search(unique_name)
        if len(name) == 0:
            self.debug.warn(f'CANNNT FIND COURSE {unique_name}')
            return None
        if len(name) > 1:
            self.debug.warn(f"CATALOG ERROR: non unique course name found: {str(name)}")
        return self.__course_list.get(name[0], None)

    def search(self, course_name:str) -> str:
        '''
        returns a list of course names that matches input
        '''
        return self.searcher.search(course_name.casefold())

    def courses(self):
        '''
        returns list of all courses within the catalog
        '''
        return self.__course_list.values()

    def course_names(self):
        '''
        returns list of all course names within the catalog
        '''
        return list(self.__course_list.keys())

    def get_degree(self, degree_name:str):
        '''
        gets degree by name
        '''
        return self.__degree_list.get(degree_name, None)

    def degrees(self):
        '''
        returns all degrees within catalog
        '''
        return self.__degree_list.values()

    def json(self):
        '''
        return catalog as a json object
        '''
        catalog = dict()
        catalog.update({'courses':list(self.__course_list.keys())})
        catalog.update({'degrees':list(self.__degree_list.keys())})
        return json.dumps(catalog)

    def __repr__(self):
        count1 = 1
        printout = ""
        for course in self.__course_list.values():
            printout+=str(count1) + ": " + repr(course) + "\n"
            count1+=1
        count1 = 1
        for degree in self.__degree_list.values():
            printout+=str(count1) + ": " + repr(degree) + "\n"
            count1+=1
        return printout

    def __str__(self):
        count1 = 1
        printout = ""
        for course in self.__course_list.values():
            printout+=str(count1) + ": " + str(course) + "\n"
            count1+=1
        count1 = 1
        for degree in self.__degree_list.values():
            printout+=str(count1) + ": " + repr(degree) + "\n"
            count1+=1
        return printout

    def __iter__(self):
        for course in self.__course_list.values():
            yield course

    def __eq__(self, other):
        if not isinstance(other, Catalog):
            return False
        return self.courses() == other.courses()

    def __len__(self):
        return len(self.__course_list)
