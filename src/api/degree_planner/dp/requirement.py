'''
requirements within templates
'''

from ..math.attributes import Attributes
from ..math.dictionary_array import Dict_Array
from ..math.array_math import array_functions as af

class Requirement():
    '''
    This class contains a template course, which contains attributes that
    serves as a filter for courses, and a course set, which is the pool of
    courses we filter from.
    '''

    specification_sets = dict() # a dictionary of 'set name' : 'specification'
    DELIMITERS = ['|', '&', '(', ')', '~', '=', '!', '@']

    def __init__(self, name, specifications=None, replacement=False, elements_required=1, credits_required=0):
        self.name = name # must be unique within a degree
        
        if specifications == None:
            specifications = ''
        self.specifications = specifications # details the attributes courses must have to fulfill this template
        self.original_specifications = specifications # just for display
        self.original_formatted_specifications = specifications # for reverting to original

        self.recommender_specifications = specifications
        self.hide_recommendations = False
        self.display = False
        self.skip = False
        self.track_resolutions = None

        self.elements_required = elements_required
        self.elements_fulfilled = 0
        self.credits_required = credits_required
        self.replacement = replacement
        self.importance = 0 # used internally by degree, higher the number the more important it is

        '''
        print(f'TESTING===')
        attr = Attributes()
        attr.add_attribute('task.A')
        attr.add_attribute('task.C')
        attr.add_attribute('task.B')
        attr2 = Attributes()
        attr2.add_attribute('banana.pudding')
        print(specification_parsing.attr_fulfills_specification('task.*', attr))
        print(specification_parsing.attr_fulfills_specification('task.*', attr2))
        '''

    def add_specification(self, specification):
        if len(self.specifications):
            self.specifications = f'({self.specifications}) & ({specification})'
        else:
            self.specifications = specification

    def replace_specifications(self, old_attr_head, new_attr):
        old_attr_head = old_attr_head.casefold()
        specification = self.specifications
        search_begin_index = 0
        while specification.find(old_attr_head, search_begin_index) != -1:
            begin_index = specification.find(old_attr_head, search_begin_index)
            end_index = af.find_set(specification, Requirement.DELIMITERS, begin_index + 1)
            if end_index == -1:
                end_index = len(specification)
            search_begin_index = end_index
            specification = specification[:begin_index] + new_attr + specification[end_index:]
        self.specifications = specification

    def wildcard_resolutions(self, elements, use_original_specifications:bool=False, use_recommender_specifications:bool=False):
        resolutions = Dict_Array(list_type='set')
        for element in elements:
            if use_recommender_specifications:
                good_match, conditions = specification_parsing.attr_fulfills_specification(self.recommender_specifications, element.attributes)
            elif use_original_specifications:
                if self.original_formatted_specifications is None:
                    self.original_formatted_specifications = self.specifications
                good_match, conditions = specification_parsing.attr_fulfills_specification(self.original_formatted_specifications, element.attributes)
            else:
                if self.specifications is None:
                    self.specifications = self.original_formatted_specifications
                good_match, conditions = specification_parsing.attr_fulfills_specification(self.specifications, element.attributes)
            if good_match:
                for wildcard_orig, wildcard_resol in conditions.items():
                    resolutions.extend_elements(wildcard_orig, wildcard_resol)
        return resolutions

    def wildcard_differentiate(self, begin_counter):
        ''' DEPRECATED, WILDCARDS WILL BECOME VARIABLES AND THUS DISTINCTNESS IS IMPLIED TO BE THE RESPONSIBILITY OF THE USER '''
        star_index = -1
        while self.specifications.find('*', star_index + 1) != -1:
            star_index = self.specifications.find('*', star_index + 1)
            delimiters = Requirement.DELIMITERS
            delimiters.append(' ')
            if star_index + 1 < len(self.specifications) and self.specifications[star_index + 1] not in delimiters:
                continue
            self.specifications = f"{self.specifications[:star_index + 1]}auto{begin_counter}{self.specifications[star_index + 1:]}"
            begin_counter += 1
        self.original_formatted_specifications = self.specifications
        return begin_counter
    
    def wildcards(self):
        '''
        untested
        '''
        wildcards = set()
        begin_index = 0
        star_index = self.specifications.find('*')
        while star_index != -1:
            begin_index = af.rfind_set(self.specifications, Requirement.DELIMITERS, 0, star_index) + 1
            end_index = af.find_set(self.specifications, Requirement.DELIMITERS, star_index)
            if end_index == -1:
                end_index = len(self.specifications)
            wildcard = self.specifications[begin_index:end_index].strip()
            wildcards.add(wildcard)
            #print(f'wildcard ---  found wildcard {wildcard} at pos {star_index}, attr begin {begin_index} end {end_index} of attr {self.specifications}')
            star_index = self.specifications.find('*', end_index)
        return wildcards

    def __repr__(self):
        string = f"Requirement {self.name}"
        return string
    
    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.elements_required)

    def __eq__(self, other):
        if not isinstance(other, Requirement):
            return False
        return self.name == other.name
    
    def __lt__(self, other):
        if not isinstance(other, Requirement):
            raise TypeError('less than comparison of requirement object against non requirement object') 
        return self.importance < other.importance

    def __gt__(self, other):
        if not isinstance(other, Requirement):
            raise TypeError('greater than comparison of requirement object against non requirement object') 
        return self.importance > other.importance

    def __add__(self, other):
        if not isinstance(other, Requirement):
            raise TypeError('addition of requirement object with non requirement object') 
        return Requirement(f'{self.name} + {other.name}', specifications=f'({self.specifications}) & ({other.specifications})', 
            replacement=self.replacement & other.replacement, courses_required=self.elements_required + other.elements_required)

    def __hash__(self):
        return hash(self.name)


class specification_parsing():

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
    def attr_fulfills_specification(specifications:str, target_attribute:Attributes):
        conditions = dict()
        if 'NA' in specifications or 'ANY' in specifications or '-1' in specifications:
            return True, {}
        if not specification_parsing.parse_attribute(specifications, target_attribute, conditions):
            return False, {}
        return True, conditions

    @staticmethod
    def single_attribute_evaluation(eval_attribute:str, target_attribute:Attributes):
        if isinstance(eval_attribute, bool):
            return eval_attribute, {}
        eval_attribute = eval_attribute.strip()
        if eval_attribute == '':
            return True, {}
        if eval_attribute in ('True', 'true'):
            return True, {}
        if eval_attribute in ('False', 'false'):
            return False, {}

        if len(eval_attribute) and eval_attribute[0] == '$':
            ''' 
            this signifies evaluate the attribute of the template with the name after $[attr] inside
            'specification sets' degree in the degrees.json
            '''
            specification = Requirement.specification_sets.get(eval_attribute[1:], None)
            if specification is None:
                return False, {}
            
            true_given_for_wildcards = {}
            truth = specification_parsing.parse_attribute(specification, target_attribute, true_given_for_wildcards)
            truth, _ = specification_parsing.single_attribute_evaluation(truth, target_attribute)
            return truth, true_given_for_wildcards
        
        if len(eval_attribute) and eval_attribute[0] == '@':
            return eval_attribute, {}

        if len(eval_attribute) and eval_attribute[-1] == '+':
            matches = target_attribute.get_attributes_ge(eval_attribute[:-1])
            return (len(matches) > 0), {}
        if len(eval_attribute) and eval_attribute[-1] == '-':
            matches = target_attribute.get_attributes_le(eval_attribute[:-1])
            return (len(matches) > 0), {}
        if '*' in eval_attribute:
            matches = target_attribute.get_attributes_by_head(eval_attribute[:eval_attribute.find('*') - 1])
            return (len(matches) > 0), {eval_attribute:matches}
        if '#' in eval_attribute:
            return (len(target_attribute.get_attributes_by_head(eval_attribute[:eval_attribute.find('#') - 1])) > 0), {}
        return (target_attribute.attr(eval_attribute) is not None), {}

    @staticmethod
    def parse_attribute(input_text:str, target_attribute:Attributes, true_given_for_wildcards:dict=None) -> str:
        '''
        Input -> Attribute
        Input -> True|False
        Input -> (Input)
        Input -> Input & Input
        Input -> Input | Input

        single_attribute_evaluation(Attribute, course) -> True|False

        returns a True or False value based on whether the course fulfills the template
        '''

        input_text = input_text.strip()
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

            new_string = input_text[: open_bracket_loc] + str(specification_parsing.parse_attribute(input_text[open_bracket_loc + 1 : close_bracket_loc], target_attribute, true_given_for_wildcards)) + input_text[close_bracket_loc + 1:]
            return specification_parsing.parse_attribute(new_string, target_attribute, true_given_for_wildcards)
        
        if '&' in input_text:
            symbol_loc = input_text.find('&')
            return specification_parsing.parse_attribute(input_text[: symbol_loc], target_attribute, true_given_for_wildcards) and specification_parsing.parse_attribute(input_text[symbol_loc + 1:], target_attribute, true_given_for_wildcards)
        
        if '|' in input_text:
            symbol_loc = input_text.find('|')
            return specification_parsing.parse_attribute(input_text[: symbol_loc], target_attribute, true_given_for_wildcards) or specification_parsing.parse_attribute(input_text[symbol_loc + 1:], target_attribute, true_given_for_wildcards)
        
        if '==' in input_text:
            symbol_loc = input_text.find('==')
            return specification_parsing.parse_attribute(input_text[: symbol_loc], target_attribute, true_given_for_wildcards) == specification_parsing.parse_attribute(input_text[symbol_loc + 2:], target_attribute, true_given_for_wildcards)
        
        if '!=' in input_text:
            symbol_loc = input_text.find('!=')

            result = specification_parsing.parse_attribute(input_text[: symbol_loc], target_attribute, true_given_for_wildcards) != specification_parsing.parse_attribute(input_text[symbol_loc + 2:], target_attribute, true_given_for_wildcards)
            return result

        if input_text.startswith('~'):
            return not specification_parsing.parse_attribute(input_text[1:], target_attribute, true_given_for_wildcards)

        truth, true_given_entries = specification_parsing.single_attribute_evaluation(input_text, target_attribute)
        #print(f'truth of {input_text}: {truth}')
        if len(true_given_entries):
            true_given_for_wildcards.update(true_given_entries)
        return truth
