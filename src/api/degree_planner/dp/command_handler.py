import re
from ..user.user import User
from ..io.output import Output
from ..dp.command import Command

class command_handler():

    @staticmethod
    def user_input(planner, user:User, user_input:str, io:Output=None, prompting=False) -> bool:
        ''' MAIN FUNCTION FOR ACCEPTING COMMAND ENTRIES

        Args:
            user (User): user object containing all user data and unique user ID
            message (str): string to be parsed as command or submitted to a waiting
                active command
            output (Output): user interface output

        Returns:
            bool: whether input was successfully executed
        '''

        if User.Flag.CMD_PAUSED in user.flag:
            ''' this means that the system is awaiting a response from the user '''
            user.command_queue_locked = True
            user.command_decision = user_input.strip().casefold()

        else:
            ''' we add a new command to the user's command queue 
            only if they're not actively processing commands '''

            if user.command_queue_locked:
                io.print(f'queue busy, please try again later')
                return False

            user.command_queue_locked = True
            user.command_queue.join()
            commands = command_handler.parse_command(user_input, io)

            for command in commands:
                user.command_queue.put(command)

        command_handler.execute_commands(planner, user, io, prompting)
        user.command_queue_locked = False
        io.debug(f'user {user.username} unlocked their command queue')
        return True

    @staticmethod
    def execute_commands(planner, user:User, io:Output=None, prompting=False) -> None:
        ''' EXECUTES COMMANDS FROM USER'S COMMAND QUEUE

        Args:
            user (User): user object containing all user data and unique user ID
            output (Output): user interface output
        '''

        """
        This while loop will keep running until all commands are executed with
        one exception: if user input is requested to finish running a command.
        
        If that is the case, this loop will break, the current command will be
        stored in User, and further user input will run this loop again where
        it first executes the stored command, and then continue as normal.
        
        NOTE: Use break to stop this loop only when awaiting user input
        and add Flag.CMD_PAUSED in user.flag, otherwise the loop can never
        be entered again.
        """
        io.debug(f'user {user.username} entered command loop')
        while(not user.command_queue.empty() or User.Flag.CMD_PAUSED in user.flag):
            if User.Flag.CMD_PAUSED in user.flag:
                command:Command = user.command_paused
            else:
                command:Command = user.command_queue.get()
                io.debug(f'user {user.username} fetched command {command}')

            if command.command == Command.CMD.IMPORT:
                io.print("begin importing data")
                planner.import_data(io)
                io.print("importing completed")
                user.command_queue.task_done()
                continue

            if command.command == Command.CMD.FIND:
                if not len(command.arguments):
                    io.print(f"no arguments found. Use find, [courses] to find courses")
                else:
                    for entry in command.arguments:
                        io.print(f"courses matching {entry}:")
                        courses = planner.find(entry)
                        i = 1
                        for course_name in courses:
                            io.print(f"{i}: {course_name}")
                            i += 1
                user.command_queue.task_done()
                continue

            if command.command == Command.CMD.SCHEDULE:
                if not len(command.arguments):
                    io.print(f"not enough arguments, please specify a schedule name")
                else:
                    schedule_name = command.arguments[0]
                    if user.get_schedule(schedule_name) is None:
                        io.print(f"creating new schedule {schedule_name}")
                        user.new_schedule(schedule_name)
                        user.set_active_schedule(schedule_name)
                    else:
                        io.print(f"switched schedule to {schedule_name}")
                        user.set_active_schedule(schedule_name)
                user.command_queue.task_done()
                continue

            # all commands after this requires an active schedule inside User
            schedule = user.get_active_schedule()
            if schedule is None:
                io.print(f"no schedule selected, creating one named {user.username}")
                user.new_schedule(user.username)
                user.set_active_schedule(user.username)
                schedule = user.get_active_schedule()

            if command.command in (Command.CMD.ADD, Command.CMD.REMOVE):
                if User.Flag.CMD_PAUSED in user.flag:
                    decision = user.command_decision
                    course_names = command.data_store
                    if not decision.isdigit() or int(decision) not in range(1, len(course_names) + 1):
                        io.print(f"Please enter a valid selection number")
                        break
                    course_name = course_names[int(decision) - 1]
                    command.arguments[1] = course_name
                    user.flag.remove(User.Flag.CMD_PAUSED)

                semester = command.arguments[0]
                course_name = command.arguments[1]
                possible_courses = planner.find(course_name)

                if not len(possible_courses):
                    io.print(f"no courses matching entry {course_name} found")

                if len(possible_courses) > 1 and prompting:
                    io.print(f"entry {course_name} has multiple choices, please choose from list:")
                    i = 1
                    for course in possible_courses:
                        io.store(f"  {i}: {course}")
                        i += 1
                    io.view_cache()
                    # pause command, set temporary variables/storage and break from the loop
                    command.data_store = possible_courses
                    user.command_paused = command
                    user.flag.add(User.Flag.CMD_PAUSED)
                    break

                if command.command == Command.CMD.ADD:
                        planner.add_course(user, semester, course_name, io)
                else:
                    planner.remove_course(user, semester, course_name, io)

                user.command_queue.task_done()
                continue

            if command.command == Command.CMD.PRINT:
                io.store(f"{str(schedule)}")
                io.view_cache()
                user.command_queue.task_done()
                continue

            if command.command == Command.CMD.DEGREE:
                if not command.arguments:
                    io.print(f"no arguments found. Use degree, <degree name> to set your schedule's degree")
                else:
                    planner.degree(user, command.arguments[0], io)
                user.command_queue.task_done()
                continue

            if command.command == Command.CMD.FULFILLMENT:
                if schedule.degree is None:
                    io.print(f"no degree specified")
                else:
                    io.store(f"{schedule.name} Fulfillment")
                    io.store(f"  taken courses: {[str(e) for e in schedule.courses()]}")
                    fulfillment = schedule.degree.fulfillment(schedule.courses())
                    io.store(Output.print_fulfillment(fulfillment))
                    io.view_cache()
                user.command_queue.task_done()
                continue

            if command.command == Command.CMD.RECOMMEND:
                if schedule.degree is None:
                    io.print(f"no degree specified")
                else:
                    io.store(f"{schedule.name} Recommended path of completion:")
                    recommendation = schedule.degree.recommend(schedule.courses(), custom_tags=command.arguments)
                    io.store(Output.print_recommendation(recommendation))
                    io.view_cache()

                user.command_queue.task_done()
                continue

            if command.command == Command.CMD.DETAILS:
                details = planner.details(command.arguments[0])
                if details is None:
                    details = 'please enter valid full name of course'
                io.store(details)
                io.view_cache()
                user.command_queue.task_done()
                continue

            if command.command == Command.CMD.CACHE:
                io.print("recomputing cache")
                planner.cache()
                io.print("finished cache recompute")
                user.command_queue.task_done()
                continue

            else:
                io.print(f"Unimplemented command {command.command} entered")
                user.command_queue.task_done()
                continue


    #--------------------------------------------------------------------------
    # HELPER FUNCTIONS
    #--------------------------------------------------------------------------
    @staticmethod
    def parse_command(cmd:str, io:Output=None) -> list:
        ''' Parse string into a list of Command objects

        Args:
            cmd (str): input string to be parsed
            output (Output): user interface output

        Returns:
            list[Command]: list of Command objects each containing data
                on command and arguments
        '''

        arg_list = [command_handler.cleanse_input(e.strip().casefold()) for e in cmd.split(",") if e.strip()]
        cmd_queue = []
        last_command = None

        for argument in arg_list:
            # if we find a command, push the last command to the queue and create new command
            if Command.CMD.get(argument) != Command.CMD.NONE:
                if last_command is not None:
                    cmd_queue.append(last_command)
                last_command = Command(argument)
            # otherwise, add this as an argument to the last command
            else:
                if last_command is not None:
                    last_command.arguments.append(argument)
                else:
                    io.print(f"ERROR: invalid command '{argument}'")
        # after exiting the loop, push the last command if it exists into the queue
        if last_command is not None:
            cmd_queue.append(last_command)

        # verify all commands have the required number of arguments
        for argument in cmd_queue:
            if not argument.valid():
                io.print(f"ERROR: invalid arguments for command {str(argument)}")
        cmd_queue = [e for e in cmd_queue if e.valid()]
        return cmd_queue

    @staticmethod
    def cleanse_input(msg:str) -> str:
        re.sub(r'\W+', '', msg)
        return msg
