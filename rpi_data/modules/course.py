import time
import pdb
import copy
from typing import overload
class Course:
    name:str
    credits:int
    days:str
    stime:int
    etime:int
    profs:str
    loc:str
    max:int
    curr:int
    rem:int
    dept:str
    sdate:str
    enddate:str
    sem:str
    crn:int 
    code:int
    section:int
    short:str
    long:str
    frequency:str
    desc:str 
    raw:str
    pre:list
    co:list
    major:str
    school:str
    lec:str
    #Info will be an array of strings: 
    # [crn, major, code, section, credits, name, days, stime, etime, max, curr, rem, profs, sdate, enddate, loc]

    def __init__(self, info):
        self.crn = info[0]
        self.major = info[1]
        self.code = info[2]
        self.section = info[3]
        self.credits = info[4]
        self.name = info[5]
        self.days = info[6]
        self.stime = info[7]
        self.etime = info[8]
        self.max = info[9]
        self.curr = info[10]
        self.rem = info[11]
        self.profs = info[12]
        self.sdate = info[13]
        self.enddate = info[14]
        self.loc = info[15]
        self.long = self.processName(self.name)
        self.short = self.major + '-' + self.code
        self.lec = "LEC"
        self.desc = ""
        self.raw = ""
        self.pre = list()
        self.co = list()
        self.school = ""
    
    def processName(self, name:str) -> str:
        tmp = name.split()
        for i in range(0, len(tmp), 1):
            if not tmp[i].isalpha():
                continue 
            tmp[i]= tmp[i][:1].upper() + tmp[i][1:].lower()
        return ' '.join(tmp)
    def addSemester(self, semester):
        self.sem = semester.upper()
    def addReqs(self, pre:list=[], co:list=[], raw:str="", desc: str=""):
        self.desc = desc
        self.raw = raw
        self.pre = copy.deepcopy(pre)
        self.co = copy.deepcopy(co)
    
    def addReqsFromList(self, info: list=[]):
        self.desc = info[0]
        self.raw = info[1]
        self.preq = info[2]
        self.co = info[3]
    def print(self):
        for attr, value in self.__dict__.items():
            print(attr, " : ", value)
    #Turn the class back into a list. 
    #Because of the diffs in how we store vs how we want it to be, need to do a lot of swapping
    #Maybe there's a diff way than doing this, hopefully there is
    def decompose(self) -> list[str]:
        retList = []
        retList.append(self.name)
        retList.append(self.lec)
        retList.append(self.credits)
        retList.append(self.days)
        retList.append(self.stime)
        retList.append(self.etime)
        retList.append(self.profs)
        retList.append(self.loc)
        retList.append(self.max)
        retList.append(self.curr)
        retList.append(self.rem)
        retList.append(self.major)
        retList.append(self.sdate)
        retList.append(self.enddate)
        retList.append(self.sem)
        retList.append(self.crn)
        retList.append(self.code)
        retList.append(self.section)
        retList.append(self.short)
        retList.append(self.long)
        retList.append(self.desc)
        retList.append(self.raw)
        retList.append(self.frequency)
        retList.append(self.pre)
        retList.append(self.co)
        retList.append(self.school)
        return retList
    def addSchool(self, school):
        self.school = school
    def __lt__(self, other):
        #Note that we will maybe need to compare times? Idk how to handle the case where the classes
        #are the same (ie lab, lecture, test) so at the moment the lecture appears last.
        #  So far we just sort in reverse order.
        if self.major > other.major:
            return self.major > other.major
        if self.code > other.code:
            return self.code > other.code
        return self.section > other.section
    
    def __str__(self):
        return self.name