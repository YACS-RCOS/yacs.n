'''
Parsing functions specific for custom data structure

You will need to make your own parser for every data input file
'''

import json
import os
from .output import Output
from ..dp.course import Course
from ..dp.catalog import Catalog
from ..dp.degree import Degree
from ..dp.template import Template

CATALOG_PATH = Output.DATA_FOLDER_PATH + "catalog.json"
DEGREE_PATH = Output.DATA_FOLDER_PATH + "degrees.json"
TAGS_PATH = Output.DATA_FOLDER_PATH + "tags.json"

print('current working directory: ' + os.getcwd())


class parsing():

    def parse_courses(catalog:Catalog, io:Output=None):
        if io is None:
            io = Output(Output.OUT.DEBUG, auto_clear=True)

        io.print("Beginning parsing course data into catalog")
        
        if os.path.isfile(CATALOG_PATH):
            io.print(f"file found: {CATALOG_PATH}")
            file_catalog_results = open(CATALOG_PATH)
        else:
            io.print("catalog file not found")
            return
        
        json_data = json.load(file_catalog_results)
        file_catalog_results.close()

        for course_data in json_data:
            course = Course(course_data['name'], course_data['subject'], course_data['course_id'])
            for attr, attr_val in course_data.items():
                if isinstance(attr_val, list):
                    for e in attr_val:
                        course.add_attribute(f"{attr}.{e}")
                else:
                    course.add_attribute(f"{attr}.{attr_val}")
            catalog.add_course(course)


    """ Rarses json data degree objects stored in Catalog

    Args:
        file_name (str): name of file to parse from
        catalog (Catalog): catalog object to store parsed information into
        output (Output): debug output, default is print to console
    """
    def parse_degrees(catalog:Catalog, io:Output=None):
        if io is None:
            io = Output(Output.OUT.DEBUG, auto_clear=True)
        io.print("Beginning parsing degree data into catalog")
        
        ''' NOT IMPLEMENTED FOR JSON INPUT YET
        There are 1 location(s) for degrees, checked in this order:
        1) data/
        '''
        if os.path.isfile(DEGREE_PATH):
            io.print(f"file found: {DEGREE_PATH}")
            file_degree = open(DEGREE_PATH)
        else:
            io.print("degree file not found")
            return
        
        degrees = json.load(file_degree)
        file_degree.close()

        for degree_name, degree_templates in degrees.items():
            # degrees
            if catalog.get_degree(degree_name) is not None:
                catalog.remove_degree(degree_name)
                io.print(f"replaced degree {degree_name} in catalog")
            degree = Degree(degree_name, catalog)
            io.print(f"added degree {str(degree)} to catalog")

            for template_name, template_properties in degree_templates.items():
                # templates within degree
                template = Template(template_name)

                for property_name, property_value in template_properties.items():
                    # property dictionary within template

                    # replacement enabled
                    if property_name == 'replacement':
                        template.replacement = property_value

                    if property_name == 'requires':
                        template.courses_required = property_value

                    # attributes for template course
                    elif property_name == 'attributes':
                        template.specifications.extend(property_value)
                degree.add_template(template)
            catalog.add_degree(degree)
            

    '''
    parses degree tags into their respective degrees within the catalog
    '''
    def parse_tags(catalog:Catalog, io:Output=None):
        if io is None:
            io = Output(Output.OUT.DEBUG, auto_clear=True)
        if os.path.isfile(TAGS_PATH):
            io.print(f"file found: {TAGS_PATH}")
            file_tags = open(TAGS_PATH)
        else:
            io.print("degree file not found")
            return
            
        tags = json.load(file_tags)
        file_tags.close()

        for subject, tag_list in tags.items():
            catalog.tags.update({subject.casefold() : list(tag_list)})
