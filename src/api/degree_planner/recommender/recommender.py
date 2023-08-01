import numpy as np
from ..math.array_math import array_functions as af
from ..recommender.cache import Cache
import logging

class Recommender():

    ATTRIBUTE_BIN = 'subject'
    ATTRIBUTE_TO_EMBED = 'name'
    ENABLE_TENSORFLOW = False

    cache = None
    cache:Cache
    scorer = None

    @staticmethod
    def initialize(catalog):
        if not Recommender.ENABLE_TENSORFLOW:
            logging.warn("Recommender.initialize() TENSOR IS DISABLED")
            return
        
        from .course_scorer import Scorer
        if Recommender.cache is None:
            Recommender.load_cache()
        Recommender.scorer = Scorer(catalog, Recommender.cache)

    @staticmethod
    def get_scorer():
        if Recommender.scorer is None:
            logging.warn("TENSORFLOW IS DISABLED")
        return Recommender.scorer

    @staticmethod
    def load_cache():
        if Recommender.cache is None:
            logging.info("creating cache")
            Recommender.cache = Cache()
        logging.info("recommender loading cache")
        Recommender.cache.load_cache()

    @staticmethod
    def recache():
        if not Recommender.ENABLE_TENSORFLOW:
            logging.warn("TENSORFLOW IS DISABLED")
            return
        if Recommender.cache is None:
            Recommender.load_cache()
        Recommender.cache.clear()
        Recommender.scorer.init_tag_relevances_to_courses()
        Recommender.cache.store_cache()

    @staticmethod
    def get_custom_tag_relevances(course, custom_tags):
        if not Recommender.ENABLE_TENSORFLOW:
            return np.zeros(len(custom_tags))
        return Recommender.scorer.get_tag_relevances(course, custom_tags)

    @staticmethod
    def embedded_relevance(selected_elements:set, all_elements:set, defined_tags:dict, custom_tags:set=None) -> dict:
    
        if Recommender.cache is None:
            Recommender.load_cache()
        relevance_all_elements = dict()
        
        ''' STEP 1: initialize dictionary of arrays that represent the relevance scores of each subject for the user '''
        relevance_tags = dict() # { bin : [relevance score] }
        for bin, tags_set in defined_tags.items():
            relevance_tags.update({bin : np.zeros(len(tags_set))})

        ''' STEP 2: compute a scaled sum of all of tag relevances of user's taken courses, organized by bin (such as course subject)
        this is to allow different tagging methods for different kinds of items to avoid irrevelant tags from influencing results '''

        for element in selected_elements:
            bin = element.attr(Recommender.ATTRIBUTE_BIN)
            relevance_tags_to_elements = Recommender.cache.tag_relevances_to_courses.get(element.name.casefold(), None)
            if relevance_tags_to_elements is None:
                continue
            af.scale_dictionary_values(relevance_tags, relevance_tags_to_elements, 1.0, key=bin)

        ''' STEP 3: normalization '''
        relevance_tags = {k: af.hard_max(v) for k, v in relevance_tags.items()}

        # printing user's preference scores
        #for bin, tags in self.catalog.tags.items():
            #self.io.debug(f"user's best descriptors for {bin}: {af.best_descriptors(dict(zip(tags, tag_relevances_to_user_by_bin.get(bin))), 5, 0.3)}")

        ''' STEP 4: compute relevance of each recommending course and compare to user's tag relevances and relevance to the custom tag '''
        for element in all_elements:
            bin = element.attr(Recommender.ATTRIBUTE_BIN)
            relevance_tags_to_elements = Recommender.cache.tag_relevances_to_courses.get(element.name.casefold(), None)
            course_relevance_to_user = 10
            if relevance_tags_to_elements is not None:
                course_relevance_to_user = af.array_similarity(relevance_tags.get(bin), relevance_tags_to_elements)
            if custom_tags is not None and Recommender.ENABLE_TENSORFLOW:
                custom_tag_relevances_to_course = Recommender.get_custom_tag_relevances(element, custom_tags) # numpy array
                custom_course_relevance_to_user = af.array_similarity(custom_tag_relevances_to_course, np.zeros(len(custom_tag_relevances_to_course)))
                course_relevance_to_user += custom_course_relevance_to_user
            
            relevance_all_elements.update({element : course_relevance_to_user})
            # element.keywords = self.cache.course_keywords.get(element.unique_name)

        return relevance_all_elements
