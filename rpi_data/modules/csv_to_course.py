import os
import csv
from course import Course
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# This file takes our csv formatting and turns it into a course class type.
# If something goes wrong it's because you changed one of those two.

def parse_csv(filename):
    courses = list()
    i = 0
    with open(os.path.join(__location__, filename), 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            if i == 0:
                i += 1
                continue
            temp = Course(["" for _ in range(16)])
            temp.name = row[0]
            temp.lec = row[1]
            temp.credits = row[2]
            temp.days = row[3]
            temp.stime = row[4]
            temp.etime = row[5]
            temp.profs = row[6]
            temp.loc = row[7]
            temp.max = row[8]
            temp.curr = row[9]
            temp.rem = row[10]
            temp.major = row[11]
            temp.sdate = row[12]
            temp.enddate = row[13]
            temp.sem = row[14]
            temp.crn = row[15]
            temp.code = row[16]
            temp.section = row[17]
            temp.short = row[18]
            temp.long = row[19]
            temp.desc = row[20]
            temp.raw = row[21]
            #empty column here
            temp.pre = row[23]
            temp.co = row[24]
            temp.school = row[25]
            courses.append(temp)
    return courses
