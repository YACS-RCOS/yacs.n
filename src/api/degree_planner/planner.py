'''
DEGREE PLANNER MAIN CLASS
'''

from .io.output import Output
from .io.parse import parsing
from .dp.catalog import Catalog
from .math.search import Search
from .dp.command_handler import command_handler
from .user.user import User

VERSION = "API 3.0 refactored generalization"

class Planner():
    '''
    All interaction with a Planner is with this class, either by calling user_input
    with a user's command or by directly accessing the functions provided here.

    One catalog is generated for each Planner

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

    def __init__(self, enable_tensorflow=True, prompting=False):
        # each user is assigned a User object and stored in this dictionary
        # Users = <user id, User>
        self.users = dict()
        self.catalog = Catalog()
        self.course_search = Search()

        self.output = Output(Output.OUT.INFO, signature='INPUT HANDLER', auto_clear=True)

        # configurable flags
        self.ENABLE_TENSORFLOW = enable_tensorflow
        self.PROMPTING = prompting
        self.SEMESTERS_MAX  = 12

    def get_user(self, userid):
        return self.users.get(userid, None)

    def add_user(self, userid, username=None):
        if userid in self.users:
            return
        self.users.update({userid:User(userid, username)})

    def remove_user(self, userid):
        self.users.pop(userid, None)

    def user_input(self, user:User, input:str) -> dict:
        '''
        returns a dictionary of variables:values to update on the frontend based on commands entered
        that changes user state (ie active schedule, active degree)
        '''
        return command_handler.user_input(self, user, input, self.output, prompting=self.PROMPTING)

    def schedule(self, user:User, schedule_name:str) -> None:
        ''' Changes user's active schedule selection and creates new schedule if
            specified schedule is not found

        Args:
            user (User): user to perform the action on
            schedule_name (str): schedule name
            output (Output): user interface output
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

    def schedules(self, user:User) -> list:
        ''' Get all of user's schedule

        Args:
            user (User): get the active schedule of this user

        Returns:
            list (list(Schedule)): returns a list of all schedule
                objects
        '''
        return user.schedules()

    def change_degree(self, user:User, degree_name:str) -> bool:
        ''' Changes user's active schedule's degree

        Args:
            user (User): user to perform the action on
            schedule (Schedule): schedule to change degree on
            degree_name (str): degree name
            output (Output): user interface output

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
        return user.get_active_schedule().courses()


    def fulfillment(self, user:User, schedule_name, io=None, wildcard_resolutions=None):
        if io is None:
            io = self.output

        schedule = user.get_schedule(schedule_name)

        if schedule is None:
            io.print(f"no schedule named {schedule_name} for user {user}")
            return f"no schedule named {schedule_name} for user {user}"

        if schedule.degree is None:
            io.print(f"no degree set for user {user}")
            return f"no degree set for user '{user.username}'"
        

        fulfillment = schedule.degree.fulfillment(schedule.courses(), wildcard_resolutions=wildcard_resolutions)
        return fulfillment


    def recommend(self, user:User, schedule_name, io=None):
        if io is None:
            io = self.output

        schedule = user.get_schedule(schedule_name)

        if schedule.degree is None:
            io.print(f"no degree specified")
            return f"no degree specified"

        recommendation = schedule.degree.recommend(schedule.courses())
        return recommendation

    def add_course(self, user:User, semester, course_name:str):
        ''' Add course to user's schedule

        Args:
            user (User): user to perform the action on
            course_name (str): course name
            semester (int or str): semester to add course into
            output (Output): user interface output

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
            output (Output): user interface output

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


    def find(self, course_name:str) -> None:
        ''' Print list of courses to output that match input entry, searches from entire catalog

        Args:
            course_name (str): search term
            output (Output): user interface output
        '''
        possible_courses = self.course_search.search(course_name)
        possible_courses.sort()
        return possible_courses


    def import_data(self) -> Exception:
        ''' Parse json data into a list of courses and degrees inside a catalog

        Args:
            output (Output): user interface output

        Returns:
            Exception: if exception occurs, returns exception, else None
        '''

        parsing.parse_courses(self.catalog, self.output)
        self.output.print(f"Sucessfully parsed catalog data")

        parsing.parse_degrees(self.catalog, self.output)
        self.output.print(f"Sucessfully parsed degree data")

        parsing.parse_tags(self.catalog, self.output)
        self.output.print(f"parsed tags")

        self.course_search.update_items(self.catalog.get_elements(), True)

        # self.catalog.reindex()


    def cache(self):
        if self.catalog.recommender is not None:
            self.catalog.recommender.recache()
