'''
sorting functions
'''

class sorting():

    @staticmethod
    def dictionary_sort(dictionary:dict, return_tuples:bool=False) -> list:
        '''
        sorts dictionary keys by their attached values
        '''
        sorted_tuples = sorted(dictionary.items(), key=lambda x:x[1])

        if return_tuples:
            return (sorted_tuples)

        sorted_list = list()
        for key, _ in sorted_tuples:
            sorted_list.append(key)

        return sorted_list
    

    @staticmethod
    def list_of_dictionary_sort(list_of_dictionaries:list, sort_by_key) -> list:
        # first, create a dictionary of the indexes and sort by values
        dict_and_key = dict()

        i = 0
        for dictionary in list_of_dictionaries:
            dict_and_key.update({i:dictionary[sort_by_key]})
            i += 1
        
        rearranged_order = sorting.dictionary_sort(dict_and_key)
        new_list = []
        for index in rearranged_order:
            new_list.append(list_of_dictionaries[index])

        return new_list


    @staticmethod
    def bucket_sort(item_and_values:dict) -> list:
        '''
        Bucket sort that sorts courses inside requested_courses by the number of bindings they have
        with courses within all_fulfillment, from least to most
        '''
        sorted = list()
        buckets = list()

        lowest_value = 0 # for offset
        for l_value in item_and_values.values():
            if l_value < lowest_value:
                lowest_value = int(l_value)

        for item, value in item_and_values.items():
            # determine the appropriate bucket to put each course in
            # generate the necessary empty buckets
            value = int(value)
            value -= lowest_value
            for _ in range(0, value - len(buckets) + 1):
                buckets.append(list())

            # append to the appropriate bucket
            buckets[value].append(item)

        # condense the buckets into a single list
        for bucket in buckets:
            sorted.extend(bucket)
        return sorted
