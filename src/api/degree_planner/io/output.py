'''
Output class
'''

import logging
from enum import Enum
import json
import os

class Output():
    '''
    Handles printing output to specified location

    Args:
        output_location (OUT): Enum that describes location to print into
        output_type (OUTTYPE): How to format output
        file (file): file to print to if printing to file
        signature (str): used for embed titles
    '''

    class OUT(Enum):
        NONE = 0

        CONSOLE = 1
        INFO = 2
        DEBUG = 3
        WARN = 4
        ERROR = 5

        STORE = 6
        FILE = 7

        VISUALIZE = 8

    class OUTTYPE(Enum):
        STRING = 1
        JSON = 2


    DATA_FOLDER_PATH = os.getcwd() + "/degree_planner/data/"
    visualizers = dict()

    @staticmethod
    def visualize(visualizer_name, *args):
        visualizer = Output.visualizers.get(visualizer_name)
        if visualizer is not None:
            visualizer.visualize(*args)


    def __init__(self, output_location:OUT, output_type:OUTTYPE=OUTTYPE.STRING, user=None, 
            file=None, signature:str=None, auto_clear=False):

        self.output_location = output_location
        self.output_type = output_type
        self.file = file
        self.user = user
        self.auto_clear = auto_clear

        self.cache = list()
        self.signature = signature

        self.DELIMITER_TITLE = ' :: '
        self.LJUSTIFY = 13


    def println(self, printout, output_location:OUT=None, file_name:str=None) -> None:
        self.print('\n' + printout, output_location=output_location, file_name=file_name)


    def print(self, printout, output_location:OUT=None, file_name:str=None, no_signature:bool=False) -> None:
        '''
        Determines appropriate printing channel and prints message

        Args:
            msg (str/dict): message to print
            
            logging_flag (OUT): temporary prints to this output location
                without altering the stored location within this object
        '''

        output_location = self.output_location if output_location == None else output_location

        if output_location == self.OUT.NONE:
            return

        if self.output_type == self.OUTTYPE.JSON:
            if isinstance(printout, dict):
                output = json.dumps(printout)
            elif isinstance(printout, str):
                output = json.dumps({'MESSAGE':printout})
            elif isinstance(printout, json):
                output = printout
        else:
            output = ''
            if isinstance(printout, dict):
                for entry_key, entry_value in printout.items():
                    output += f'{entry_key}{self.DELIMITER_TITLE}{entry_value}\n'
            elif isinstance(printout, str):
                if not no_signature and not self.signature is None and len(self.signature):
                    output = f'{self.signature.ljust(self.LJUSTIFY) if self.LJUSTIFY != 0 else self.signature}{self.DELIMITER_TITLE}{printout}'
                else:
                    output = printout
            elif isinstance(printout, json):
                output = str(json.loads(printout))

            if output_location == self.OUT.INFO:
                logging.info(output)
            elif output_location == self.OUT.DEBUG:
                logging.debug(output)
            elif output_location == self.OUT.WARN:
                logging.warning(output)
            elif output_location == self.OUT.ERROR:
                logging.error(output)
            elif output_location == self.OUT.CONSOLE:
                print(output)

        if (output_location == self.OUT.STORE):
            self.cache.append(output)

        elif (output_location == self.OUT.FILE):
            if file_name is None:
                file_name = self.file
            f = open(file_name, 'a')
            f.write(output)
            f.close


    def store(self, printout):
        self.print(printout, self.OUT.STORE, no_signature=True)

    def view_cache(self, output_redirect=None) -> None:
        '''
        prints cache
        '''
        if output_redirect == None:
            for line in self.cache:
                self.print(line, no_signature=True)
        else:
            for line in self.cache:
                self.print(line, output_location=output_redirect, no_signature=True)
        
        if self.auto_clear:
            self.cache.clear()

    def peek_cache(self, output_redirect=None) -> None:
        '''
        print the most recent entry in cache
        '''
        if not len(self.cache):
            return
        if output_redirect == None:
            self.print(self.cache[-1], no_signature=True)
        else:
            self.print(self.cache[-1], output_redirect=output_redirect, no_signature=True)

        if self.auto_clear:
            self.cache.pop(-1)

    def get_cache(self) -> list:
        cache = self.cache
        self.cache = list()
        return cache

    def debug(self, data) :
        self.print(data, output_location=self.OUT.DEBUG)
    
    def info(self, data):
        self.print(data, output_location=self.OUT.INFO)
    
    def warn(self, data):
        self.print(data, output_location=self.OUT.WARN)
    
    def error(self, data):
        self.print(data, output_location=self.OUT.ERROR)



    ######################################
    # PRINT FORMATTING
    ######################################

    @staticmethod
    def format_fulfillments(fulfillments) -> list:
        
        formatted_fulfillments = list()
        
        for fulfillment in fulfillments.values():
            formatted = dict()
            formatted.update({'name':fulfillment.template.name})
            formatted.update({'replacement':fulfillment.template.replacement})
            formatted.update({'required_count':fulfillment.get_required_count()})
            formatted.update({'actual_count':fulfillment.get_actual_count()})
            formatted.update({'specifications':fulfillment.template.specifications})
            fulfillment_set = [str(course) for course in fulfillment.get_fulfillment_set()]
            formatted.update({'fulfillment_set':fulfillment_set})
            formatted.update({'alternatives':fulfillment.template.wildcard_choices})

            formatted_fulfillments.append(formatted)
        
        return formatted_fulfillments

    @staticmethod
    def print_fulfillment(all_fulfillment:dict, as_dict=False) -> str:
        '''
        Print fulfillment dictionary in a neat string format
        '''
        if isinstance(all_fulfillment, str):
            if as_dict:
                return {'error':all_fulfillment}
            return all_fulfillment

        printout = ''
        if as_dict:
            printout = dict()
        fulfillments = list(all_fulfillment.values())
        fulfillments.sort()
        for status in fulfillments:
            if as_dict:
                printout.update({status.template.name:[str(e) for e in status.get_fulfillment_set()]})
            else:
                printout += (f"  Template '{status.template.name}':" + \
                    f"\n    replacement: {status.template.replacement}, importance: {status.template.importance}" + \
                    f"\n    required count: {status.get_required_count()}" + \
                    f"\n    actual count: {status.get_actual_count()}" + \
                    f"\n    specifications: {status.template.specifications}" + \
                    f"\n    original specifications: {status.template.original_specifications}\n")
                simplified_fulfillment_set = set()
                for course in status.get_fulfillment_set():
                    simplified_fulfillment_set.add(course.get_unique_name())
                printout += f"    fulfillment set: {simplified_fulfillment_set}\n"
        return printout
    
    @staticmethod
    def format_recommendations(recommendation:dict) -> list:

        formatted_recommendations = list()

        templates = list(recommendation.keys())
        templates.sort()
        templates.reverse()
        for template in templates:
            for generated_template, fulfillment_courses in recommendation.get(template).items():
                formatted = dict()
                formatted.update({'name':generated_template.name})
                formatted.update({'specifications':generated_template.specifications})
                formatted.update({'courses_fulfilled':generated_template.courses_fulfilled})
                fulfillment_set = [str(e) for e in fulfillment_courses]
                del fulfillment_set[5:]
                formatted.update({'fulfillment_set':fulfillment_set})
                formatted_recommendations.append(formatted)

        return formatted_recommendations


    @staticmethod
    def print_recommendation(recommendation:dict, as_dict=False) -> str:
        '''
        Print recommendation dictionary in a neat string format
        '''
        if isinstance(recommendation, str):
            if as_dict:
                return {'error':recommendation}
            return recommendation
        
        if as_dict:
            printout = dict()
            templates = list(recommendation.keys())
            templates.sort()
            templates.reverse()
            for template in templates:
                for generated_template, fulfillment_courses in recommendation.get(template).items():
                    printout.update({f"{generated_template.name}":f"specifications: {generated_template.specifications}" + \
                    f"fulfillment courses: {[str(e) for e in fulfillment_courses]}"})
            return printout

        printout = ''
        templates = list(recommendation.keys())
        templates.sort()
        templates.reverse()
        for template in templates:
            printout += (f"\n  Original Template '{template.name}':" + \
                f"\n    replacement: {template.replacement}, importance: {template.importance}" + \
                f"\n    required count: {template.get_required_count()}" + \
                f"\n    specifications: {template.specifications}\n")
            
            for generated_template, fulfillment_courses in recommendation.get(template).items():
                printout += (f"\n    Generated Template '{generated_template.name}':" + \
                f"\n      specifications: {generated_template.specifications}" + \
                f"\n      fulfillment courses: {[str(e) for e in fulfillment_courses]}\n")

        return printout
