import copy

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
    # [crn, major, code, section, credits, name, days, stime,
    # etime, max, curr, rem, profs, sdate, enddate, loc]

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
        self.long = self.process_name(self.name)
        self.frequency = ""
        self.short = self.major + '-' + self.code
        self.lec = "LEC"
        self.desc = ""
        self.raw = ""
        self.pre = list()
        self.co = list()
        self.school = ""
        self.sem = ""

    def process_name(self, name:str) -> str:
        tmp = name.split()
        for i in range(0, len(tmp), 1):
            if not tmp[i].isalpha():
                continue
            tmp[i]= tmp[i][:1].upper() + tmp[i][1:].lower()
        return ' '.join(tmp)

    def add_semester(self, semester):
        self.sem = semester.upper()

    def add_reqs(self, pre:list=None, co:list=None, raw:str="", desc: str=""):
        if pre is None:
            pre = []
        if co is None:
            co = []
        self.desc = desc
        self.raw = raw
        self.pre = copy.deepcopy(pre)
        self.co = copy.deepcopy(co)

    def add_reqs_from_list(self, info:list=None):
        if info is None:
            info = []
        self.pre = info[0]
        self.co = info[1]
        self.raw = info[2]
        self.desc = info[3]

    def print(self):
        for attr, value in self.__dict__.items():
            print(attr, " : ", value)
    #Turn the class back into a list.
    #Because of the diffs in how we store vs how we want it to be, need to do a lot of swapping
    #Maybe there's a diff way than doing this, hopefully there is
    def decompose(self) -> list[str]:
        ret_list = []
        ret_list.append(self.name)
        ret_list.append(self.lec)
        ret_list.append(self.credits)
        ret_list.append(self.days)
        ret_list.append(self.stime)
        ret_list.append(self.etime)
        ret_list.append(self.profs)
        ret_list.append(self.loc)
        ret_list.append(self.max)
        ret_list.append(self.curr)
        ret_list.append(self.rem)
        ret_list.append(self.major)
        ret_list.append(self.sdate)
        ret_list.append(self.enddate)
        ret_list.append(self.sem)
        ret_list.append(self.crn)
        ret_list.append(self.code)
        ret_list.append(self.section)
        ret_list.append(self.short)
        ret_list.append(self.long)
        ret_list.append(self.desc)
        ret_list.append(self.raw)
        ret_list.append(self.frequency)
        ret_list.append(self.pre)
        ret_list.append(self.co)
        ret_list.append(self.school)
        return ret_list

    def list_to_class(self, row):
        self.name = row[0]
        self.lec = row[1]
        self.credits = row[2]
        self.days = row[3]
        self.stime = row[4]
        self.etime = row[5]
        self.profs = row[6]
        self.loc = row[7]
        self.max = row[8]
        self.curr = row[9]
        self.rem = row[10]
        self.major = row[11]
        self.sdate = row[12]
        self.enddate = row[13]
        self.sem = row[14]
        self.crn = row[15]
        self.code = row[16]
        self.section = row[17]
        self.short = row[18]
        self.long = row[19]
        self.desc = row[20]
        self.raw = row[21]
        self.pre = row[23]
        self.co = row[24]
        self.school = row[25]

    def add_school(self, school):
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
