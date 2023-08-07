'''
DEGREE PLANNER MAIN CLASS
'''

from .io.output import Output
from .io.parse import parsing
from .dp.catalog import Catalog
from .math.search import Search
from .user.user import User
from .dp.recommend import recommend
from .dp.fulfill import get_fulfillment, get_optimized_fulfillment
from .recommender.recommender import Recommender

VERSION = "API 3.0 refactored generalization"

class Planner():
    '''
    All interaction with a Planner is with this class, either by calling user_input
    with a user's command or by directly accessing the functions provided here.

    Valid commands are:
        (developer only)
            import
                - parse course and degree information from json
            cache
                - recomputes cache with the courses/tags within catalog

        (general use)
            schedule, <schedule name>
                - set active schedule. New schedule will be created if
                specified schedule does not exist
            degree, <degree name>
                - set degree of active schedule
            add, <semester>, <course name>
                - add course to active schedule, courses may not duplicate
                within the same semester but may duplicate accross semesters
            remove, <semester>, <course name>
                - remove course from active schedule in specified semester
            print
                - print schedule
            fulfillment
                - print degree requirement fulfillment status
            recommend
                - recommend courses based on courses already taken. Can also
                recommend based on custom inputs, but requires tensorflow
                to be enabled
            find, <course>* (may list any number of courses)
                - find courses that match with the inputted string. Useful
                for browsing courses that contain certain keywords.
            details, <course>
                - course description

    NOTE: This class is created once and is not instigated for each user.
    It is essential to keep all user specific data inside the User class.
    '''

    def __init__(self, enable_tensorflow=True):
        # each user is assigned a User object and stored in this dictionary
        # Users = <user id, User>
        self.users = dict()
        self.catalog = Catalog()
        self.course_search = Search()

        self.subject_groups = None

        self.output = Output(Output.OUT.INFO, signature='INPUT HANDLER', auto_clear=True)

        # configurable flags
        self.ENABLE_TENSORFLOW = enable_tensorflow
        if enable_tensorflow:
            Recommender.ENABLE_TENSORFLOW = True
        self.SEMESTERS_MAX  = 12

    def get_user(self, userid) -> User:
        return self.users.get(userid, None)

    def add_user(self, userid, username=None):
        if userid in self.users:
            return
        self.users.update({userid:User(userid, username)})

    def remove_user(self, userid):
        self.users.pop(userid, None)

    def schedule(self, user:User, schedule_name:str) -> None:
        ''' Changes user's active schedule selection and creates new schedule if
            specified schedule is not found

        Args:
            user (User): user to perform the action on
            schedule_name (str): schedule name
        '''
        schedule = user.get_schedule(schedule_name)
        if schedule is None:
            self.output.print(f"Schedule {schedule_name} not found, generating new one!")
            user.new_schedule(schedule_name)
            user.set_active_schedule(schedule_name)
            return
        else:
            self.output.print(f"Successfully switched to schedule {schedule_name}!")
            user.set_active_schedule(schedule_name)
            return
        
    def delete_schedule(self, user:User, schedule_name:str) -> None:
        schedule = user.get_schedule(schedule_name)
        if schedule is not None:
            user.remove_schedule(schedule_name)
            self.output.print(f"Deleting {schedule_name}, user's schedules: {user.get_schedule_names()}")
        else:
            self.output.print(f"Schedule {schedule_name} not found")

    def rename_schedule(self, user:User, old_name, new_name) -> None:
        schedule = user.get_schedule(old_name)
        if schedule is not None:
            user.rename_schedule(old_name, new_name)
            self.output.print(f"Renamed schedule {old_name} to {new_name}")
        else:
            self.output.print(f"Schedule {old_name} not found")


    def schedules(self, user:User) -> list:
        ''' Get all of user's schedule

        Args:
            user (User): get the active schedule of this user

        Returns:
            list (list(Schedule)): returns a list of all schedule
                objects
        '''
        return user.get_schedule_names()

    def set_degree(self, user:User, degree_name:str) -> bool:
        ''' Changes user's active schedule's degree

        Args:
            user (User): user to perform the action on
            schedule (Schedule): schedule to change degree on
            degree_name (str): degree name

        Returns:
            bool: if degree was successfully changed.
                False usually means specified degree was not found
        '''
        degree = self.catalog.get_template(degree_name)

        if degree is None:
            self.output.print(f"invalid degree entered: {degree_name}")
            return False
        
        user.get_active_schedule().degree = degree
        self.output.print(f"set your degree to {degree.name}")
        return True

    def selected_elements(self, user:User) -> set:
        return user.get_active_schedule().get_courses()


    def fulfillment(self, user:User, schedule_name, wildcard_resolutions=None):
        schedule = user.get_schedule(schedule_name)
        if schedule is None:
            self.output.error(f"no schedule named {schedule_name} for user {user}")
            return f"no schedule named {schedule_name} for user {user}"

        if schedule.degree is None:
            self.output.error(f"no degree set for user {user}")
            return f"no degree set for user '{user.username}'"

        fulfillment = get_optimized_fulfillment(schedule.get_courses(), schedule.degree.requirements, wildcard_resolutions)
        return fulfillment


    def recommend(self, user:User, schedule_name, custom_tags=None):
        schedule = user.get_schedule(schedule_name)
        if schedule.degree is None:
            self.output.print(f"no degree specified")
            return f"no degree specified"

        recommendation = recommend(schedule.get_courses(), self.catalog, schedule.degree.requirements, custom_tags=custom_tags)
        return recommendation

    def add_course(self, user:User, semester, course_name:str):
        ''' Add course to user's schedule

        Args:
            user (User): user to perform the action on
            course_name (str): course name
            semester (int or str): semester to add course into

        Returns:
            returned_courses (list): If there are multiple courses that match course_name, 
                then this list will be returned in the form of a list of Courses.
        '''
        
        # sanity checks
        if not semester.isdigit() or int(semester) not in range(0, self.SEMESTERS_MAX):
            self.output.error(f"Invalid semester {semester}, enter number between 0 and {self.SEMESTERS_MAX}")
            return

        # list of courses matching course_name
        semester = int(semester)
        matched_course_names = self.find(course_name)

        if len(matched_course_names) != 1:
            return

        # at this point, returned_courses have exactly one course, so we can perform the addition immediately
        course = matched_course_names[0]
        user.get_active_schedule().add_course(semester, self.catalog.get_element(course))
        self.output.debug(f"Added course {course} to semester {semester}")


    def remove_course(self, user:User, semester, course_name:str):
        ''' Remove course from user's schedule

        Args:
            user (User): user to perform the action on
            course_name (str): course name
            semester (int or str): semester to remove course from

        Returns:
            returned_courses (list): If there are multiple courses that match course_name, 
                then this list will be returned in the form of a list of Courses.
        '''

        if not semester.isdigit() or int(semester) not in range(0, self.SEMESTERS_MAX):
            self.output.error(f"Invalid semester {semester}, enter number between 0 and {self.SEMESTERS_MAX}")
            return

        semester = int(semester)
        matched_course_names = self.find(course_name)

        if len(matched_course_names) != 1:
            return

        course = matched_course_names[0]
        user.get_active_schedule().remove_course(semester, self.catalog.get_element(course))
        self.output.debug(f"Removed course {course} from semester {semester}")


    def find(self, course_name:str) -> list:
        ''' returns matches as sorted list '''
        possible_courses = self.course_search.search(course_name)
        possible_courses.sort()
        return possible_courses


    def import_data(self) -> Exception:
        ''' Parse json data into a list of courses and degrees inside a catalog

        Returns:
            Exception: if exception occurs, returns exception, else None
        '''

        parsing.parse_catalog(self.catalog)
        self.output.print(f"Sucessfully parsed catalog data")

        parsing.parse_templates(self.catalog)
        self.output.print(f"Sucessfully parsed degree data")

        parsing.parse_tags(self.catalog)
        self.output.print(f"parsed tags")

        self.subject_groups = parsing.parse_subject_groups()
        self.output.print(f"parsed subject groups")
        self.index()

    def index(self):
        self.course_search.update_items(self.catalog.get_elements(), True)
        self.course_search.generate_index()

    def recache(self):
        Recommender.initialize(self.catalog)
        Recommender.recache()
