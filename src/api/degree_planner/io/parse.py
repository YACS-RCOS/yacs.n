'''
Parsing functions specific for custom data structure

You will need to make your own parser for every data input file
'''

import os
import json
import logging
from .output import Output
from ..dp.element import Element
from ..dp.catalog import Catalog
from ..dp.requirement import Requirement
from ..dp.template import Template
from ..math.dictionary_array import Dict_Array

CATALOG_PATH = Output.DATA_FOLDER_PATH + "catalog.json"
TEMPLATES_PATH = Output.DATA_FOLDER_PATH + "degrees.json"
TAGS_PATH = Output.DATA_FOLDER_PATH + "tags.json"

logging.info('current working directory: ' + os.getcwd())

class parsing():

    @staticmethod
    def parse_catalog(catalog:Catalog):
        logging.info("Beginning parsing course data into catalog")
        
        if os.path.isfile(CATALOG_PATH):
            logging.info(f"file found: {CATALOG_PATH}")
            file_catalog_results = open(CATALOG_PATH)
        else:
            logging.error("catalog file not found")
            return
        
        json_data = json.load(file_catalog_results)
        file_catalog_results.close()

        for element_data in json_data:
            element = Element(f"{element_data['subject']} {element_data['course_id']} {element_data['name']}")
            level = element_data['course_id'][0]
            element.attributes.add_attribute(f"level.{level}")
            for attr, attr_val in element_data.items():
                if isinstance(attr_val, list):
                    for e in attr_val:
                        element.attributes.add_attribute(f"{attr}.{e}")
                else:
                    element.attributes.add_attribute(f"{attr}.{attr_val}")
            catalog.add(element)

    @staticmethod
    def parse_templates(catalog:Catalog):
        ''' Rarses json data degree objects stored in Catalog

        Args:
            file_name (str): name of file to parse from
            catalog (Catalog): catalog object to store parsed information into
        '''
        logging.info("Beginning parsing degree data into catalog")

        if os.path.isfile(TEMPLATES_PATH):
            logging.info(f"file found: {TEMPLATES_PATH}")
            file_templates = open(TEMPLATES_PATH)
        else:
            logging.error("templates file not found")
            return
        
        templates = json.load(file_templates)
        file_templates.close()

        group_credit_requirements = dict()

        for template_name, template_data in templates.items():
            # degrees

            if catalog.get_template(template_name) is not None:
                catalog.remove_template(template_name)
                logging.debug(f"replaced template {template_name} in catalog")
            template = Template(template_name)
            logging.info(f"added template {str(template)} to catalog")

            wildcard_diff_counter = 0
            requirement_importance_counter = 1000

            template_group_credit_requirements = dict()

            for requirement_name, requirement_properties in template_data.items():

                if requirement_name == 'groups':
                    for property_name, property_value in requirement_properties.items():
                        template_group_credit_requirements.update({property_name:property_value})
                    group_credit_requirements.update({template_name:template_group_credit_requirements})
                    continue

                # templates within degree
                requirement = Requirement(requirement_name)
                requirement.importance = requirement_importance_counter
                requirement_importance_counter -= 1

                for property_name, property_value in requirement_properties.items():
                    # property dictionary within template

                    # replacement enabled
                    if property_name == 'replacement':
                        requirement.replacement = property_value

                    elif property_name == 'requires':
                        requirement.elements_required = property_value

                    # attributes for template course
                    elif property_name == 'specifications':
                        requirement.specifications = property_value

                    elif property_name == 'credits':
                        requirement.credits_required = property_value

                requirement.original_specifications = requirement.specifications
                wildcard_diff_counter = requirement.wildcard_differentiate(wildcard_diff_counter)

                template.requirements.append(requirement)
            catalog.add(template)

        # make groups
        for template in catalog.get_templates():
            template:Template
            groups = Dict_Array()
            for requirement in template.requirements:
                requirement:Requirement
                group_name = requirement.name.split('-')[0].strip()
                groups.add(group_name, requirement)

            for group_name, requirements in groups.dictionary.items():
                credits_required = 0
                if template.name in group_credit_requirements:
                    credits_required = group_credit_requirements.get(template.name).get(group_name, 0)
                template.groups.append({'name':group_name, 'credits_required':credits_required, 'requirements':requirements})


        # parse specification sets
        spec_sets = catalog.get_template('specification sets')
        if spec_sets is not None:
            print('importing specification sets')
            for requirement in spec_sets.requirements:
                requirement:Requirement
                print(f'added specification {requirement.name} with specifications {requirement.specifications}')
                Requirement.specification_sets.update({requirement.name:requirement.specifications})
            catalog.remove_template('specification sets')
            
    @staticmethod
    def parse_tags(catalog:Catalog):
        ''' parses template tags into their respective degrees within the catalog '''

        if os.path.isfile(TAGS_PATH):
            logging.info(f"file found: {TAGS_PATH}")
            file_tags = open(TAGS_PATH)
        else:
            logging.error("tags file not found")
            return
            
        tags = json.load(file_tags)
        file_tags.close()

        for subject, tag_list in tags.items():
            catalog.tags.update({subject.casefold() : list(tag_list)})
