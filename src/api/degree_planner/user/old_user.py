'''
User class and Flag enum that indicates command queue status for the user
'''

from enum import Enum
import json
from queue import Queue
from ..user.schedule import Schedule

class User():
    '''
    Stores user identification, schedules, course eligibility and command queue operatons info
    '''
    def __init__(self, id, username=None):
        self.id = id # unique id for user
        self.username = username # username to display
        if self.username is None:
            self.username = id
        self.__schedules = dict() # all schedules this user created <schedule name, Schedule>
        self.active_schedule = "" # name of schedule to modify

        self.flag = set()

        # command queue handling
        self.command_queue = Queue()
        self.command_queue_locked = False
        self.command_decision = None
        self.command_paused = None

    class Flag(Enum):
        '''
        For command queue use
        '''
        CMD_PAUSED = 100
        CMD_RUNNING = 101


    def schedules(self) -> list:
        '''
        Creates a copied list of all current schedule objects
        '''
        return list(self.__schedules.values())


    def get_schedule(self, schedule_name:str) -> Schedule:
        '''
        Returns schedule if found, otherwise None
        '''
        return self.__schedules.get(schedule_name, None)


    def new_schedule(self, schedule_name:str) -> None:
        '''
        Creates a new schedule if the schedule does not yet exist
        '''
        schedule = Schedule(schedule_name)
        self.__schedules.update({schedule_name : schedule})


    def add_schedule(self, schedule_name:str, schedule:Schedule):
        '''
        Add schedule from input to schedules
        '''
        self.__schedules.update({schedule_name : schedule})


    def get_active_schedule(self) -> Schedule:
        '''
        Get schedule being actively editted for this user
        '''
        return self.get_schedule(self.active_schedule)


    def set_active_schedule(self, schedule):
        if isinstance(schedule, Schedule):
            schedule = schedule.name
        if schedule in self.__schedules:
            self.active_schedule = schedule


    def rename_schedule(self, old_name:str, new_name:str) -> bool:
        '''
        Renames existing schedule only if new name does not already exist

        Returns:
            success (bool): whether rename was successful
        '''
        if old_name not in self.__schedules or new_name in self.__schedules:
            return False
        else:
            self.__schedules.update({new_name : self.__schedules.get(old_name)})
            self.__schedules.pop(old_name)
            return True

    def json(self) -> json:
        '''
        Creates json file of this class
        '''
        user = dict()
        user.update({'username':self.username})
        user.update({'id':self.id})
        schedules = list()
        for s in self.__schedules.keys():
            schedules.append(s)
        user.update({'schedules':schedules})
        user.update({'commands in queue':self.command_queue.qsize()})
        return json.dumps(user)

    def __repr__(self):
        schedule_names = ""
        for s in self.__schedules.keys():
            schedule_names += f"[ {s} ] "
        return f"{str(self.username)}'s schedules: {schedule_names}"


    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        if self.username == other.username:
            return True
        return False


    def __hash__(self):
        return hash(self.id)
