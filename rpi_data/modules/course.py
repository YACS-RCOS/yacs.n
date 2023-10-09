from dataclasses import dataclass
#A class to store all the relevant info we need to put in the csv
#see https://stackoverflow.com/questions/47955263/what-are-data-classes-and-how-are-they-different-from-common-classes
@dataclass
class Course:
    def __init__(self, name:str, credits:int, days:str, stime:int, etime:int,
            profs:str, loc:str, max:int, curr:int, rem:int, dept:str,sdate:str, enddate:str,
            sem:str, crn:int, code:int, section:int, short:str, long:str,
            desc:str, raw:str, pre:str, co:str,major:str) -> None:
        self.short = major + code
        self.long = processName(name)
    def processName(name:str) -> str:
        tmp = name.split()
        for word in tmp:
            word.lower()
            word[0].upper()
        return ''.join(tmp)
    def print():
        for attr, value in self.__dict__.items():
            print(attr, " : ", value)