'''
Command class and command enums
'''

from enum import Enum

class Command():
    '''
    User command object, contains the command as a enum
    and a list of arguments
    '''

    class CMD(Enum):
        '''
        Command Enum
        '''

        # the number presents minimum number of arguments for that command
        ADD = '2.add'
        REMOVE = '2.remove'
        SCHEDULE = '1.schedule'
        PRINT = '0.print'
        FULFILLMENT = '0.fulfillment'
        RECOMMEND = '0.recommend'
        DEGREE = '1.degree '
        FIND = '1.find'
        DETAILS = '1.details'
        CACHE = '0.cache'

        INFO = '0.info'
        IMPORT = '0.import'
        TAG = '1.tag'
        NONE = '0.none'
    
        @staticmethod
        def get(string:str):
            '''
            gets command enum from string

            Returns:
                cmd enum (CMD): matched enum, CMD.NONE if cannot find enum
            '''
            try:
                enum = Command.CMD[string.upper()]
            except:
                enum = Command.CMD.NONE
            return enum

    def __init__(self, command:str):
        self.command = Command.CMD.get(command)
        self.arguments = []
        self.data_store = None

    def valid(self) -> bool:
        '''
        A valid command means there are at least the number of required arguments
        stored in this command. The amount of arguments required is stored as the
        first digit in the enum value
        '''
        return int(self.command.value[0]) <= len(self.arguments)

    def __len__(self):
        return len(self.arguments) + 1

    def __repr__(self):
        return f"{', '.join([str(self.command)] + self.arguments)}"

    def __eq__(self, other):
        if not isinstance(other, Command):
            return False
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))
