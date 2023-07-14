import json
import os
import numpy as np
from ..io.output import Output

CACHE_PATH = os.getcwd() + '/degree_planner/data/cache.json'

class Cache():

    def __init__(self, cache_file_name=None):
        self.cache_file_name = cache_file_name
        # {course: embedding}
        self.course_embeddings = dict()
        
        # {tag : embedding}
        self.tag_embeddings = dict()
        
        # {course : [dist]} distances to the embedding of all tags for all course embeddings
        self.tag_relevances_to_courses = dict()
        
        # {course : [keyword]}
        self.course_keywords = dict()

        # {word: embedding}
        self.word_embeddings = dict()

        self.debug = Output(Output.OUT.DEBUG, auto_clear=True)


    def load_cache(self):
    
        self.debug.print(f"LOADING CACHE...", Output.OUT.INFO)

        if os.path.isfile(CACHE_PATH):
            self.debug.print(f"file found: {CACHE_PATH}")
            file_embedding_cache = open(CACHE_PATH)
        else:
            self.debug.print("cache file not found", Output.OUT.WARN)
            return

        try:
            json_data = json.load(file_embedding_cache)
            for cache_category, cache in json_data.items():
                if not isinstance(cache, dict):
                    self.debug.print(f'error: cache data {cache_category} not a dictionary')
                    continue
                if cache_category.casefold() == 'course_embeddings':
                    self.course_embeddings = {key:np.array(value) for key, value in cache.items()}
                if cache_category.casefold() == 'tag_embeddings':
                    self.tag_embeddings = {key:np.array(value) for key, value in cache.items()}
                if cache_category.casefold() == 'tag_relevances_to_courses':
                    self.tag_relevances_to_courses = {key:np.array(value) for key, value in cache.items()}
                if cache_category.casefold() == 'course_keywords':
                    self.course_keywords = cache
                if cache_category.casefold() == 'word_embeddings':
                    self.word_embeddings = {key:np.array(value) for key, value in cache.items()}

        except Exception as e:
            self.debug.print(f"FAILED TO IMPORT CACHE, exception {e}", Output.OUT.WARN)
        
        file_embedding_cache.close()


    def store_cache(self):
        cache = dict()
        cache.update({'course_embeddings':{key:value.tolist() for key, value in self.course_embeddings.items()}})
        cache.update({'tags_embeddings':{key:value.tolist() for key, value in self.tag_embeddings.items()}})
        cache.update({'tag_relevances_to_courses':{key:value.tolist() for key, value in self.tag_relevances_to_courses.items()}})
        cache.update({'course_keywords':self.course_keywords})
        cache.update({'word_embeddings':{key:value.tolist() for key, value in self.word_embeddings.items()}})
        cache_json = json.dumps(cache)
        self.write_to_file(CACHE_PATH, cache_json)


    def clear(self):
        self.course_embeddings.clear()
        self.tag_embeddings.clear()
        self.tag_relevances_to_courses.clear()
        self.course_keywords.clear()
        self.word_embeddings.clear()
        self.write_to_file(CACHE_PATH, "")
        

    def write_to_file(self, file, text):
        if os.path.isfile(file):
            self.debug.print(f"file found: {file}")
        else:
            self.debug.print("file not found")
            return
        with open(file, "w") as output_file:
            output_file.write(text)
        output_file.close()


    def __len__(self):
        return (len(self.course_embeddings) + len(self.tag_embeddings) + len(self.tag_relevances_to_courses)
            + len(self.course_keywords) + len(self.word_embeddings))
