import numpy as np
import copy
from .sorting import sorting


class array_functions():

    @staticmethod
    def array_similarity(vec1, vec2):
        return np.linalg.norm(np.add(vec1, np.multiply(vec2, -1))).item()

    @staticmethod
    def soft_max(x):
        sum = 0
        for i in range(0, len(x)):
            sum += np.exp(x[i])
        for i in range(0, len(x)):
            x[i] = (np.exp(x[i])) / sum
        return x

    @staticmethod
    def hard_max(x, adjust=0.95):
        sum = 0
        for i in range(0, len(x)):
            sum += np.exp(x[i]) - adjust
        for i in range(0, len(x)):
            x[i] = (np.exp(x[i]) - adjust ) / sum
        return x

    @staticmethod
    def scale_array(array, additive, multiplicative):
        return np.add(np.dot(array, multiplicative), additive)

    @staticmethod
    def scale_dictionary_values(dictionary, additive, multiplicative, key=None):
        if key is not None:
            dictionary.update({key : array_functions.scale_array(dictionary.get(key), additive, multiplicative)})
            return
        for key in dictionary.keys():
            dictionary.update({key : array_functions.scale_array(dictionary.get(key), additive, multiplicative)})

    @staticmethod
    def best_descriptors(descriptors, amount:int, threshold:float):
        sorted_descriptors = sorting.dictionary_sort(descriptors, True)[:amount]
        best_descriptors = list()
        for tag, tag_relevance in sorted_descriptors:
            if tag_relevance < threshold:
                best_descriptors.append(f'{tag} ({int(1 / tag_relevance)}%)')
        return best_descriptors

    @staticmethod
    def generate_combinatorics(bound:list, start_index=1) -> list:
        '''
        recursively generates a list of all combinations from picking a wildcard evaluation possibility

        e.g. suppose degree with two templates, 1) level.* and 2) subject.* resolves into
        1) level.1, level.4 and 2) subject.csci, subject.biol for a certain user

        this will return a list of 
        [[level.1, subject.csci], [level.1, subject.biol], [level.4, subject.csci], [level.4, subject.biol]]

        Returns:
            list: contains all possible combinations
        '''
        if len(bound) == 0:
            return [[]]
        bound_cpy = copy.copy(bound)
        last_num = bound_cpy.pop(-1)
        nth_combo = []
        for i in range(start_index, last_num + start_index):
            prev_combos = array_functions.generate_combinatorics(bound_cpy)
            for prev_combo in prev_combos:
                prev_combo.append(i)
                nth_combo.append(prev_combo)
        return nth_combo
