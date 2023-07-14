import numpy as np
from ..math.array_math import array_functions as af
from .cache import Cache
from ..io.output import Output
from .embed import Sentence_Embedder

class Scorer():

    def __init__(self, catalog, cache:Cache):
        self.catalog  = catalog
        self.cache = cache
        self.embedder = Sentence_Embedder()

        ''' HYPERPARAMETERS '''
        self.ATTRIBUTE_BIN = 'subject'
        self.ATTRIBUTE_TO_EMBED = 'name'
        self.BEST_DESCRIPTORS_AMOUNT = 3
        self.BEST_DESCRIPTORS_THRESHOLD = 0.1
        self.debug = Output(Output.OUT.DEBUG)

    def init_word_embeddings(self):
        pass

    def get_course_embedding(self, course, cache=True):
        course_embedding = self.cache.course_embeddings.get(course.unique_name, None)
        if course_embedding is None:
            course_embedding = self.embed_message(course.attr(self.ATTRIBUTE_TO_EMBED))
            if cache:
                self.cache.course_embeddings.update({course.unique_name:course_embedding})
        return course_embedding

    def get_tag_embedding(self, tag, cache=True):
        tag_embedding = self.cache.tag_embeddings.get(tag, None)
        if tag_embedding is None:
            tag_embedding = self.embed_message(tag)
            if cache:
                self.cache.tag_embeddings.update({tag:tag_embedding})
        return tag_embedding

    def get_tag_relevances(self, course, tags, cache=True):
        tag_relevances_to_course = np.zeros(len(tags))
        for i in range(len(tags)):
            # fetch tag embedding or create it if not already created
            tag = tags[i]
            tag_relevances_to_course[i] = af.array_similarity(self.get_course_embedding(course, cache), self.get_tag_embedding(tag, cache))
        return tag_relevances_to_course

    def normalize(self, array):
        smallest_num = min(array)
        array = np.add(array, - (smallest_num - 0.01))
        array = af.hard_max(array)
        return array

    def init_tag_relevances_to_courses(self, normalize=True):
        '''
        this function allows both precomputing of premade tags and on the fly computation of custom tags
        given by the user. 

        Precomputed tag relevances (as well as their respective tag and course embeddings) are cached,
        while custom tag relevances will only be returned and not stored.
        '''

        for course in self.catalog.courses():

            ''' STEP 1: DETERMINE BIN TO PUT COURSE IN AND WHAT TAGS TO COMPUTE
            
            a set of tag is associated with a bin, in the case of the degree planner, a subject
            since it's most optimal to use a different set of tags catered to its subject '''
            if self.ATTRIBUTE_BIN is None:
                bin = 'default'
            else:
                bin = course.attr(self.ATTRIBUTE_BIN)

            tags = self.catalog.tags.get(bin)
            if tags is None:
                # if it's still None, then we end
                continue

            ''' STEP 2: fetch/calculate all tag and course embeddings and generate relevance array
            by comparing every tag embedding to the course embedding '''
            tag_relevances_to_course = self.get_tag_relevances(course, tags, True)

            ''' STEP 3: adjust relevance such that the most relevant score is drastically better than the others.
            this is because a small change in the embedding can represent a large jump in similarity '''
            if normalize:
                tag_relevances_to_course = self.normalize(tag_relevances_to_course)

            ''' STEP 4: find the best descriptors for this course by finding tags with high relevance '''
            descriptors = dict(zip(self.catalog.tags.get(bin), tag_relevances_to_course))
            self.cache.course_keywords.update({course.unique_name : af.best_descriptors(descriptors, self.BEST_DESCRIPTORS_AMOUNT, self.BEST_DESCRIPTORS_THRESHOLD)})
            ''' STEP 5: update the tag relevances to course value within cache '''
            self.cache.tag_relevances_to_courses.update({course.unique_name : tag_relevances_to_course})


    def embed_message(self, message):
        return_as_list = True
        if not isinstance(message, list):
            return_as_list = False
            message = [message]
        embedded_messages = self.embedder.embed(message)
        if return_as_list:
            return embedded_messages
        return np.array(embedded_messages[0])
