'''
General use constant time search

(currently uses fixed size index so technically only constant time
up to a degree, i.e. < 10000 elements)
'''

class Search():
    '''
    Generates search index to enable constant time search of element by name
    '''

    def __init__(self, items_list:set=None, convert_items_to_string=False):
        if items_list is None: items_list = set()

        if convert_items_to_string:
            self.__items = set()
            for i in items_list:
                self.__items.add(str(i))
        else:
            self.__items = items_list

        self.__index = dict()
        self.INDEXED_LENGTH = 3
        self.generate_index()

    def generate_index(self) -> None:
        '''
        generates {key : {all possible items' full name} }
        where key is the first 3 letters of each of the words in its name
        must be called everytime items get updated
        '''
        self.__index.clear()
        for name in self.__items:
            words = name.split(' ')

            for word in words:
                if len(word) < self.INDEXED_LENGTH:
                    continue

                #this is add three letter key only
                word_key = word[0:self.INDEXED_LENGTH].casefold()
                if(word_key not in self.__index.keys()):
                    self.__index.update({word_key:{name}})
                else:
                    self.__index[word_key].add(name)


    def update_items(self, item_set, convert_items_to_string=False):
        if convert_items_to_string:
            self.__items = set()
            for i in item_set:
                self.__items.add(str(i))
        else:
            self.__items = item_set


    def search(self, msg) -> list:
        ''' 
        Searches for possible items based on msg,
        taking into account only words inside msg of 3 letters and above
        '''
        words = msg.split(' ')
        results = []

        '''
        checks first 3 letters of each word from user's input against __index
        to find items that contains all the words' keys

        Example using courses:
        <"Alg" : [course1, course2]>
        <"Int" : [course1, course3]>
        If user input was "Int Alg" or "Intro Algorithms",
        then we add course1 to possible_courses
        '''

        for word in words:
            if len(word) < self.INDEXED_LENGTH:
                continue
            key = word[0:self.INDEXED_LENGTH]
            if key not in self.__index:
                return []
            if len(results) == 0:
                results = self.__index[key]
            else:
                results = [e for e in results if e in self.__index[key]]

        # go through results to verify their entire name is within the search term
        for word in words:
            results = [e for e in results if word.casefold() in e.casefold()]                 

        return results
