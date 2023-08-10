'''
User class and Flag enum that indicates command queue status for the user
'''

from enum import Enum
from queue import Queue
from .schedule import Schedule

class User():
    '''
    Stores user identification, schedules, course eligibility and command queue operatons info
    '''
    def __init__(self, id, username=None):
        self.id = id # unique id for user
        self.username = username # username to display
        if self.username is None:
            self.username = id
        self.schedules = dict() # all schedules this user created <schedule name, Schedule>
        self.active_schedule = "" # name of schedule to modify

        self.flag = set()

        # command queue handling
        self.command_queue = Queue()
        self.command_queue_locked = False
        self.command_decision = None
        self.command_paused = None

    class Flag(Enum):
        ''' For command queue use '''
        CMD_PAUSED = 100
        CMD_RUNNING = 101

    def get_schedules(self) -> list:
        ''' Creates a copied list of all current schedule objects '''
        return list(self.schedules.values())
    
    def get_schedule_names(self):
        return list(self.schedules.keys())

    def get_schedule(self, schedule_name:str) -> Schedule:
        ''' Returns schedule if found, otherwise None '''
        return self.schedules.get(schedule_name, None)

    def new_schedule(self, schedule_name:str) -> None:
        ''' Creates a new schedule if the schedule does not yet exist '''
        schedule = Schedule(schedule_name)
        self.schedules.update({schedule_name : schedule})

    def add_schedule(self, schedule_name:str, schedule:Schedule) -> None:
        ''' Add schedule from input to schedules '''
        self.schedules.update({schedule_name : schedule})

    def remove_schedule(self, schedule_name) -> None:
        if self.active_schedule == schedule_name:
            self.active_schedule = ''
        result = self.schedules.pop(schedule_name, None)
        print(f"attempting to remove schedule {schedule_name}, result: {result}, schedules: {self.schedules}")

    def get_active_schedule(self) -> Schedule:
        ''' Get schedule object being actively editted for this user '''
        return self.get_schedule(self.active_schedule)

    def set_active_schedule(self, schedule):
        if isinstance(schedule, Schedule):
            schedule = schedule.name
        if schedule in self.schedules:
            self.active_schedule = schedule

    def rename_schedule(self, old_name:str, new_name:str) -> bool:
        '''
        Renames existing schedule only if new name does not already exist

        Returns:
            success (bool): whether rename was successful
        '''
        autoswitch = False
        if old_name == self.active_schedule:
            autoswitch = True
        if old_name not in self.schedules or new_name in self.schedules:
            return False
        else:
            schedule = self.schedules.get(old_name)
            self.schedules.update({new_name : schedule})
            self.schedules.pop(old_name)
            schedule.name = new_name

            if autoswitch:
                self.active_schedule = new_name
            return True

    def __repr__(self):
        return f"{str(self.username)}'s schedules: {','.join(self.schedules.keys())}"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
