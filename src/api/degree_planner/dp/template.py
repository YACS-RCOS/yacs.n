'''
Course Template object
'''

import copy
from .course import Course
from .fulfillment_status import Fulfillment_Status
from ..math.dictionary_array import Dict_Array

class Template():
    '''
    This class contains a template course, which contains attributes that
    serves as a filter for courses, and a course set, which is the pool of
    courses we filter from.
    '''

    specification_sets = dict() # a dictionary of 'set name' : 'specification'

    def __init__(self, name, specifications=None, replacement=False, courses_required=1):
        if specifications == None:
            specifications = list()
        elif isinstance(specifications, str):
            specifications = [specifications]
        elif isinstance(specifications, set):
            specifications = list(specifications)

        self.name = name # must be unique within a degree
        self.specifications = specifications # details the attributes courses must have to fulfill this template
        self.original_specifications = None # wildcard deconstruction modifies the specifications, so we store a copy of the original for later use
        self.courses_required = courses_required
        self.wildcard_choices = list()

        self.courses_fulfilled = 0

        self.replacement = replacement
        self.importance = 0 # used internally by degree, higher the number the more important it is

    def add_specification(self, attr):
        self.specifications.append(attr)

    def remove_specification(self, attr):
        self.specifications.remove(attr, None)

    def replace_specifications(self, old_attr_head, new_attr):
        for i in range(0, len(self.specifications)):
            specification = self.specifications[i]
            print('old specification: ' + specification)
            search_begin_index = 0
            while specification.find(old_attr_head, search_begin_index) != -1:
                begin_index = specification.find(old_attr_head)
                end_index = self.find_from_set(specification, [' ', '|', '&', '(', ')', '~'], begin_index + 1)
                if end_index != -1:
                    end_index +=1
                else:
                    end_index = len(specification)
                search_begin_index = end_index
                specification = specification[:begin_index] + new_attr + specification[end_index:]
            print('new specification: ' + specification)
            self.specifications[i] = specification


    def find_from_set(self, string, charset, begin_index=0, end_index=None):
        min_loc = len(string)
        if end_index is None:
            end_index = len(string)

        for c in charset:
            loc = string.find(c, begin_index, end_index)
            if loc != -1 and loc < min_loc:
                min_loc = loc
        if min_loc == len(string):
            return -1
        return min_loc


    def get_required_count(self):
        return self.courses_required
    

    def wildcard_resolutions(self, courses):

        resolutions = Dict_Array(list_type='set')
        
        for course in courses:
            good_match, conditions = template_parsing.course_fulfills_template(self, course)
            if good_match:
                for wildcard_orig, wildcard_resol in conditions.items():
                    resolutions.extend_elements(wildcard_orig, wildcard_resol)
        return resolutions

    def wildcard_differentiate(self, begin_counter):
        
        for i in range(len(self.specifications)):
            star_index = -1
            while self.specifications[i].find('*', star_index + 1) != -1:
                star_index = self.specifications[i].find('*', star_index + 1)
                if star_index + 1 < len(self.specifications[i]) and self.specifications[i][star_index + 1] not in (' ', ')', '(', '&', '|', '~'):
                    continue
                self.specifications[i] = self.specifications[i][:star_index + 1] + 'auto' + str(begin_counter) + self.specifications[i][star_index + 1:]
                begin_counter += 1
        return begin_counter



    def get_course_match(self, courses) -> list:
        '''
        Finds all courses that fulfills the given template

        Wildcards (*) may be used to dictate the fact that all courses within this template's fulfillment
        set must have the same values for that attribute. It doesn't matter which one, just so long as
        it's consistent. This is useful if we want a rule that says all courses must be in the same subject
        area or all courses must be in the same concentration/focus area, but doesn't matter which specific 
        one in particular.

        For example, concentration.* means all courses must be within the same concentration.
        If course1 has attribute concentration.1 and course2 has attribute concentration.1 and concentration.2,
        this function will return a list of fulfillment sets as follows:

        Template1.1 [concentration.1] : fulfillment courses: [course1, course2]
        Template1.2 [concentration.2] : fulfillment courses: [course2]

        Note that just because two courses fulfills bin.1 and only one fulfills bin.2 in this scenario doesn't
        necessarily bin.1 is a better choice. Suppose another template, Template2, which does not allow replacement
        and is of higher importance requires course1. now, both Template1.1 and Template1.2 will only have one 
        fulfillment course. This is why we must try every single combination.

        If the template doesn't contain a wildcard operator, the list would simply be a single entry
        '''

        fulfillment_sets = list() # all possible fulfillments based on different combinations resulting from wildcard sauge
        all_conditions = dict() # all possible wildcard replacement conditions that can influence the result (wildcard branching)

        # current fulfillment set, will be added only if current template does not contain wildcards
        # (recursive calls remove one wildcard at a time), so essentially "leaf" branches
        # get to add their fulfillment to fulfillment_sets
        curr_fulfillment = Fulfillment_Status(self, self.courses_required, set())

        for course in courses:
            good_match, conditions = template_parsing.course_fulfills_template(self, course)

            # updates all_conditions with possible values for wildcard replacement
            for condition, condition_sat_set in conditions.items():
                current_condition_set = all_conditions.get(condition, set())
                current_condition_set.update(condition_sat_set)
                all_conditions.update({condition:current_condition_set})

            # if this is a leaf call (no wildcard branching), add to current fulfillment set
            if good_match and not len(conditions):
                curr_fulfillment.add_fulfillment_course(course)

        # if this is a leaf call (no wildcard branching), add to main fulfillment set
        if not len(all_conditions):
            fulfillment_sets.append(curr_fulfillment)

        if self.original_specifications is None:
            self.original_specifications = copy.deepcopy(self.specifications)


        # if there are wildcard branching needed (we only need to pop the first one, the rest is handled by the following recursive calls
        # as each recursive call only needs to handle one)
        if not len(all_conditions):
            return fulfillment_sets
        wildcard_attr, wildcard_choices = all_conditions.popitem()
        print(f'WILDCARD ATTRIBUTE {wildcard_attr} RESOLVING TO CHOICES {wildcard_choices}')
        self.wildcard_choices = list(wildcard_choices)
        if len(wildcard_choices):
            self.wildcard_choices.insert(0, wildcard_attr)

        for choice in wildcard_choices:
            # for each branching choice, make a copy of the template with the wildcard replaced with a possible value
            template_cpy = copy.deepcopy(self)

            # a temporary dictionary holding the old/new values, since we cannot update an object
            # while iterating through it
            replace_attributes = dict()

            for attribute_str in template_cpy.specifications:
                if wildcard_attr not in attribute_str:
                    continue

                # we make a note of the replacements needed by storing it in replace_attributes
                attribute_str_update = attribute_str.replace(wildcard_attr, choice)
                replace_attributes.update({attribute_str:attribute_str_update})

            # we commit the changes to the specifications while iterating through the replace_attributes we made previously
            for old, new in replace_attributes.items():
                template_cpy.specifications.remove(old)
                template_cpy.specifications.append(new)

            # recursively call this function, we're guaranteed that the final return values all are wildcard-free
            fulfillment_sets.extend(template_cpy.get_course_match(courses))

        return fulfillment_sets


    def __repr__(self):
        string = f"Template {self.name}:\n"
        string += f"  replacement: {self.replacement}\n"
        string += f"  specifications: {str(self.specifications)}"
        return string
    
    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.courses_required)

    def __eq__(self, other):
        if not isinstance(other, Template):
            return False
        
        return self.name == other.name and self.specifications == other.specifications
    
    def __lt__(self, other):
        return self.importance < other.importance

    def __gt__(self, other):
        return self.importance > other.importance

    def __add__(self, other):
        new_specifications = copy.deepcopy(self.specifications)
        new_specifications.extend(other.specifications)
        return Template(f'{self.name} + {other.name}', specifications=new_specifications, 
            replacement=self.replacement & other.replacement, courses_required=self.courses_required + other.courses_required)

    def __hash__(self):
        return hash(self.name) + len(self.specifications)


class template_parsing():

    ###################################################################################################
    #
    # CONTEXT FREE PARSING
    #
    ###################################################################################################

    '''
    determines whether a course fulfills a template attribute. If it's a conditional fulfillment, then 
    also returns the condition (return type is (bool, dict))
    '''

    @staticmethod
    def course_fulfills_template(template:Template, course:Course):
        conditions = dict()
        for attr in template.specifications:
            if 'NA' in attr or 'ANY' in attr or '-1' in attr:
                continue
            if not template_parsing.parse_attribute(attr, course, conditions):
                return False, {}
        return True, conditions

    @staticmethod
    def single_attribute_evaluation(attr:str, course:Course):
        if isinstance(attr, bool):
            return attr
        attr = attr.strip()
        if attr == '':
            return True, {}
        if attr in ('True', 'true'):
            return True, {}
        if attr in ('False', 'false'):
            return False, {}

        if len(attr) and attr[0] == '$':
            ''' 
            this signifies evaluate the attribute of the template with the name after $[attr] inside
            'specification sets' degree in the degrees.json
            '''
            specification = Template.specification_sets.get(attr[1:], None)
            if specification is None:
                return False
            
            true_given_for_wildcards = {}
            truth = template_parsing.parse_attribute(specification, course, true_given_for_wildcards)
            return template_parsing.single_attribute_evaluation(truth, course), true_given_for_wildcards

        if len(attr) and attr[-1] == '+':
            matches = course.get_attributes_ge(attr[:-1])
            return (len(matches) > 0), {}
        if len(attr) and attr[-1] == '-':
            matches = course.get_attributes_le(attr[:-1])
            return (len(matches) > 0), {}
        if '*' in attr:
            matches = course.get_attributes_by_head(attr[:attr.find('*') - 1])
            return (len(matches) > 0), {attr:matches}
        if '#' in attr:
            return (len(course.get_attributes_by_head(attr[:attr.find('#') - 1])) > 0), {}
        return (course.attr(attr) is not None), {}

    @staticmethod
    def parse_attribute(input_text:str, course:Course, true_given_for_wildcards:dict=None) -> str:
        '''
        Input -> Attribute
        Input -> True|False
        Input -> (Input)
        Input -> Input & Input
        Input -> Input | Input

        single_attribute_evaluation(Attribute, course) -> True|False

        returns a True or False value based on whether the course fulfills the template
        '''
        # print('accepted input ' + str(input))

        if '(' in input_text:
            open_bracket_loc = input_text.find('(')
            close_bracket_loc = len(input_text) # we allow close brackets to be omitted if it's at the end of the input
            passed_bracket_count = 0

            # calculate the location of the closing bracket for the current bracket
            for i in range(open_bracket_loc + 1, len(input_text)):
                if input_text[i] == '(':
                    passed_bracket_count += 1
                if input_text[i] == ')':
                    if passed_bracket_count == 0:
                        close_bracket_loc = i
                        break
                    passed_bracket_count -= 1

            new_string = input_text[: open_bracket_loc] + str(template_parsing.parse_attribute(input_text[open_bracket_loc + 1 : close_bracket_loc], course, true_given_for_wildcards)) + input_text[close_bracket_loc + 1:]
            return template_parsing.parse_attribute(new_string, course, true_given_for_wildcards)
        
        if '&' in input_text:
            and_loc = input_text.find('&')
            return template_parsing.parse_attribute(input_text[: and_loc], course, true_given_for_wildcards) and template_parsing.parse_attribute(input_text[and_loc + 1:], course, true_given_for_wildcards)
        
        if '|' in input_text:
            and_loc = input_text.find('|')
            return template_parsing.parse_attribute(input_text[: and_loc], course, true_given_for_wildcards) or template_parsing.parse_attribute(input_text[and_loc + 1:], course, true_given_for_wildcards)

        if len(input_text) and input_text[0] == '~':
            return not template_parsing.parse_attribute(input_text[1:], course, true_given_for_wildcards)

        truth, true_given_entries = template_parsing.single_attribute_evaluation(input_text, course)
        if len(true_given_entries):
            true_given_for_wildcards.update(true_given_entries)
        return truth
