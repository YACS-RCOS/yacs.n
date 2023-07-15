from ..math.dictionary_array import Dict_Array

class Schedule():

    def __init__(self, name):

        self.name = name
        self.courses = Dict_Array(list_type="set")
        self.degree = None

    def add_course(self, semester, course):
        self.courses.add(semester, course)

    def remove_course(self, semester, course):
        self.courses.remove(semester, course)

    def get_courses(self, semester=None):
        if semester is None:
            return set(self.courses.elements())
        return self.courses.get(semester, set())

    def find_course(self, course):
        return self.courses.find_element(course)
    
    def __len__(self):
        return len(self.courses)
    
    def __eq__(self, other):
        if not isinstance(other, Schedule):
            return False
        return self.courses == other.courses
    
    def __repr__(self):
        return f"Schedule {self.name}, degree {self.degree} \n{self.courses}"
    
    def __hash__(self):
        return hash(self.name)
