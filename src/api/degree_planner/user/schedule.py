'''
Schedule class
'''

import json
from ..dp.course import Course

class Schedule():
    '''
    this class is created for each schedule. A user should be able to
    create multiple schedules. A schedule may contain user specific data

    TODO: add export function that transfers course lists between schedules
    without transferring any user specific data
    '''

    def __init__(self, name:str, SEMESTERS_MAX:int=12):
        # 2D list, 1st dimension is semesters and 2nd dimension is courses for that semester
        # NOTE: duplications are allowed both within semester and across semesters!
        self.courses_by_semester = list()
        self.SEMESTERS_MAX = SEMESTERS_MAX
        self.name = name
        self.degree = None

        # courses_by_semester must be initiated before use
        self.courses_list_init()


    def courses_list_init(self):
        ''' 
        Initializes the list storing all courses in the schedule, grouped by semester
        '''
        self.courses_by_semester.clear()
        for _ in range(0, self.SEMESTERS_MAX):
            self.courses_by_semester.append([])


    def add_course(self, semester, course:Course) -> bool:
        '''
        Args:
            course (Course): course to add
            semester (int): add course only to this semester

        Returns:
            success (set): whether add was successful
        '''
        if semester in self.find_course(course):
            return False
        else:
            self.courses_by_semester[semester].append(course)
            return True


    def remove_course(self, semester, course:Course) -> bool:
        '''
        Args:
            course (Course): course to remove
            semester (int): remove course only from specified semester

        Returns:
            success (bool): whether removal was successful
        '''
        if semester not in self.find_course(course):
            return False
        else:
            self.courses_by_semester[semester].remove(course)
            return True


    def get_semester(self, semester:int) -> list:
        '''
        Args:
            semester (int): semester to find courses in
        Returns:
            courses (list): all courses in the specified semester,
                None if invalid semester entered and empty list if
                semester exists but no courses added.
        '''
        if semester not in range(0, self.SEMESTERS_MAX):
            return None
        else:
            return self.courses_by_semester[semester]


    def courses(self) -> set:
        '''
        Returns:
            courses (set): all courses within this schedule
        '''
        courses = set()
        for a in self.courses_by_semester:
            for c in a:
                courses.add(c)
        return courses


    def find_course(self, course:Course) -> list:
        '''
        Args:
            course (Course): course to locate

        Returns:
            present_in (list): list of semesters that the course is found in
        '''
        i = 0
        present_in = []
        for courselist in self.courses_by_semester:
            if course in courselist:
                present_in.append(i)
            i+=1
        return present_in


    def json(self):
        '''
        Returns:
            schedule (dict): returns user's schedule in the form of
                <schedule name : <semester : course list>>
        '''
        schedule = dict()
        schedule.update({self.name:dict()})
        for i in range(0, self.SEMESTERS_MAX):
            schedule[self.name].update({i:[e.get_unique_name() for e in self.get_semester(i)]})
        return json.dumps(schedule)

    def __len__(self):
        i = 0
        for sem in self.courses_by_semester:
            i += len(sem)
        return i

    def __eq__(self, other):
        if not isinstance(other, Schedule):
            return False
        return self.courses_by_semester == other.courses_by_semester

    def __repr__(self):
        count = 0
        s = f"Schedule: {self.name} [{self.degree.name if self.degree != None else ''}]\n"
        for courselist in self.courses_by_semester:
            s+=f"  Semester {str(count)}:\n"
            count+=1
            for course in courselist:
                s+=f"    Course info: {course.get_subject()} {str(course.get_id())} {course.get_name()}\n"
        return s

    def __hash__(self):
        i = hash(self.degree)
        sem = 0
        for sem in self.courses_by_semester:
            for course in sem:
                i += hash(course) * sem
            sem += 1
        return i
