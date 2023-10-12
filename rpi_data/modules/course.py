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
    desc:str 
    raw:str
    pre:str
    co:str
    major:str
    #Info will be an array of strings:
    # [name,credits,days,stime,etime,profs,loc,max,curr,rem,dept,sdate,enddate,semester TODO:ADD,crn,course_level TODO: Get from short name,section,short,long,desc,raw,prereq,coreq,school]
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
    
    def processName(self, name:str) -> str:
        tmp = name.split()
        for word in tmp:
            word.lower()
            word[0].upper()
        return ''.join(tmp)

    def addReqs(self, pre, co, raw, desc):
        self.desc = desc
        self.raw = raw
        self.pre = pre
        self.co = co
    def print(self,):
        for attr, value in self.__dict__.items():
            print(attr, " : ", value)
    
    def __lt__(self, other):
        if self.major < other.major:
            return (self.major < other.major)
        if self.code < other.code:
            return self.code < other.code
        if self.section < other.section:
            return self.section < other.section
        if other.stime == "TBA": # TODO: I changed this from time to stime, make sure this is correct
            return True
        if self.stime == "TBA":
            return False
        return self.stime < other.stime