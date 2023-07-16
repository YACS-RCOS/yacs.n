import numpy as np
from ..math.array_math import array_functions as af
from ..io.output import Output
from ..recommender.cache import Cache

class Recommender():

    def __init__(self, catalog, cache_path=None, enable_tensorflow=True):
        self.ATTRIBUTE_BIN = 'subject'
        self.ATTRIBUTE_TO_EMBED = 'name'
        self.ENABLE_TENSORFLOW = enable_tensorflow
        self.CACHE_PATH = cache_path

        self.io = Output(Output.OUT.CONSOLE, auto_clear=True)

        self.catalog = catalog
        self.cache = None
        self.scorer = None

        if enable_tensorflow:
            from .course_scorer import Scorer
            if self.cache is None:
                self.load_cache()
            self.scorer = Scorer(self.catalog, self.cache)


    def get_scorer(self):
        if self.scorer is None:
            self.io.warn("TENSORFLOW IS DISABLED")
        return self.scorer
    

    def create_cache(self):
        self.cache = Cache(self.CACHE_PATH)
    

    def load_cache(self):
        if self.cache is None:
            self.io.info("creating cache")
            self.create_cache()
        self.io.info("recommender loading cache")
        self.cache.load_cache()


    def recache(self):
        scorer = self.get_scorer()
        if self.cache is None:
            self.load_cache()
        if scorer is None:
            self.io.warn("RECOMPUTE CACHE HALTED DUE TO TENSORFLOW DISABLED (no scorer found), NO CHANGES TO STORED CACHE MADE")
            return
        self.cache.clear()
        scorer.init_tag_relevances_to_courses()
        self.cache.store_cache()


    def get_custom_tag_relevances(self, course, custom_tags):
        scorer = self.get_scorer()
        if scorer is None:
            return np.zeros(len(custom_tags))
        return scorer.get_tag_relevances(course, custom_tags)


    def embedded_relevance(self, selected_elements:set, all_elemenets:set, custom_tags:set) -> dict:
    
        if self.cache is None:
            self.load_cache()
        relevance_all_elements = dict()
        
        ''' STEP 1: initialize dictionary of arrays that represent the relevance scores of each subject for the user '''
        relevance_tags = dict() # { bin : [relevance score] }
        for bin, tags_set in self.catalog.tags.items():
            relevance_tags.update({bin : np.zeros(len(tags_set))})

        ''' STEP 2: compute a scaled sum of all of tag relevances of user's taken courses, organized by bin (such as course subject)
        this is to allow different tagging methods for different kinds of items to avoid irrevelant tags from influencing results '''
        for element in selected_elements:
            bin = element.attr(self.ATTRIBUTE_BIN)
            relevance_tags_to_elements = self.cache.tag_relevances_to_courses.get(element.name, None)
            if relevance_tags_to_elements is None:
                continue
            af.scale_dictionary_values(relevance_tags, relevance_tags_to_elements, 1.0, key=bin)

        ''' STEP 3: normalization '''
        relevance_tags = {k: af.hard_max(v) for k, v in relevance_tags.items()}

        # printing user's preference scores
        #for bin, tags in self.catalog.tags.items():
            #self.io.debug(f"user's best descriptors for {bin}: {af.best_descriptors(dict(zip(tags, tag_relevances_to_user_by_bin.get(bin))), 5, 0.3)}")

        ''' STEP 4: compute relevance of each recommending course and compare to user's tag relevances and relevance to the custom tag '''
        for element in all_elemenets:
            bin = element.attr(self.ATTRIBUTE_BIN)
            relevance_tags_to_elements = self.cache.tag_relevances_to_courses.get(element.name, None)
            course_relevance_to_user = 10
            if relevance_tags_to_elements is not None:
                course_relevance_to_user = af.array_similarity(relevance_tags.get(bin), relevance_tags_to_elements)
            
            if custom_tags is not None and self.ENABLE_TENSORFLOW:
                custom_tag_relevances_to_course = self.get_custom_tag_relevances(element, custom_tags) # numpy array
                custom_course_relevance_to_user = af.array_similarity(custom_tag_relevances_to_course, np.zeros(len(custom_tag_relevances_to_course)))
                course_relevance_to_user += custom_course_relevance_to_user
            
            relevance_all_elements.update({element : course_relevance_to_user})
            # element.keywords = self.cache.course_keywords.get(element.unique_name)

        return relevance_all_elements
    