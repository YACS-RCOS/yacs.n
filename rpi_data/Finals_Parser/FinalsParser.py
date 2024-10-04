#!/usr/bin/env python
# coding: utf-8

# ASSUMPTIONS/DOCUMENTATION:
# 
#     - A null section value indicates that all sections share that exam date and time.
#     - Some ARCH courses list section as "80". No clue what this means.
#     - The process uses the FinalsBySubject.pdf document from the RPI website.
#         - This pdf should have columns Department, Course, Location, Date, and Grades Due (although the first and last don't matter)
#         - It should also be titled at the top of each page with Season Year followed by any amount more text (doesn't matter)
#         - If the above are not true, small modifications must be made to the process
#     - To handle inconsistent AM/PM labeling we assume that all exams begin at or after 8 AM and we assume all exams end at or before 10 PM
#     - The current process assumes the finals document is named finals_by_subject.pdf and is in the same folder as this process
#     - The output is a csv file with format: ['Season', 'Year', 'Major', 'Course', 'Section', 'Start', 'End', 'Building', 'Room_Number']
# 
# TODO:
# 
#     - Make grades due column not break the program - can't be fixed without more filled out version of exam schedule

# In[31]:


from pypdf import PdfReader
import os
from datetime import datetime
import pandas as pd
import re
import calendar
debug_mode = False


# In[32]:


# Construct a dictionary to get the number of a month from it's word
months = list(calendar.month_name)
months = [x.lower() for x in months]

# Turns a time, day of month, month, and year into one datetime object for the table
# Does this for both the start and end time for an exam
# This is used to get the start and end times for an exam
def handle_times(start_text, end_text, day, month, year):
    # Regex to get the hour and minute as seperate values from a string of the format HH:MM AM or HH:MM PM
    start_nums = re.findall(r'\d+', start_text)
    start_nums = [int(x) for x in start_nums]
    end_nums = re.findall(r'\d+', end_text)
    end_nums = [int(x) for x in end_nums]
    # Instead of trying to track AM/PM we instead use the logic that exams only happen between 8AM - 9:30 PM and convert to military time
    # This is done because RPI likes to have typos such as 8:00 M instead of 8:00 PM making the AM/PM values unreliable
    if end_nums[0] <= 10:
        end_nums[0] += 12
    if start_nums[0] < 8:
        start_nums[0] += 12
    month_num = months.index(month.lower())
    # Construct and return the datetime object
    start_text = year + str(month_num) + day + str(start_nums[0]) + ":" + str(start_nums[1])
    end_text = year + str(month_num) + day + str(end_nums[0]) + ":" + str(end_nums[1])
    format = '%Y%m%d%H:%M'
    start_time = datetime.strptime(start_text, format)
    end_time = datetime.strptime(end_text, format)
    return start_time, end_time


# In[33]:


def parser():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    reader = PdfReader("finals_by_subject.pdf")
    number_of_pages = len(reader.pages)
    
    db_lines = []

    # Process the document page by page
    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout")
        # Process the text to handle the following cases:
        #   - If the location is "TBA" we replace this with "TBA TBA" since location is Room RoomNumber
        #   - If the location is "ONLINE" we replace this with "ONLINE NA" for the same reason (Room=ONLINE,RoomNumber=NA) 
        #   - If there are "/" in the text we remove surrounding spaces so they don't cause issues (multiple different issues)
        #   - Remove the word "SECTIONS" as it's superflous and inconsistent
        text = text.replace(" / ", "/").replace("TBA", "TBA TBA").replace("ONLINE", "ONLINE NA").replace("(ALL ", "(ALL").replace("SECTIONS ", "")
        # Split text into lines, get the season (Fall,Summer,Spring) and year (20__) from the first line, then remove the first three lines since they are header/bank
        text = text.split('\n')
        for_year = text[0].split(" ")
        for_year = [x for x in for_year if x != '']
        season = for_year[0]
        year = for_year[1]
        text.pop(0)
        text.pop(0)
        text.pop(0)
        # Remove a fourth line for the first page only since it has the column headers
        if "DEPARTMENT" in text[0] and "COURSE" in text[0]:
            text.pop(0)
    
        # Now, parse the lines
        for line in text:
    
            # Remove (in SQL syntax) anything like "(NEEDS%)" because a few random courses say (NEEDS 6 HR BLOCK) or something along those lines
            while "(NEEDS" in line:
                tmp = line[line.index("(NEEDS"):]
                line = line[0:line.index("(NEEDS")] + line[line.index("(NEEDS") + tmp.index(")") + 1:]
    
            # Clean up the line and remove department
            line = line.strip()
            line = line.split(" ")
            line = [x for x in line if x != '']
            line.pop(0)
    
            # Look for the first number in the line - this will be the course code
            first_num = -1
            for i in range(len(line)):
                if any(char.isdigit() for char in line[i]):
                    first_num = i
                    break
            # Remove everything before the school code (ARCH, CSCI, etc)
            for i in range(first_num - 1):
                line.pop(0)
            # Get major
            major = line[0]
            line.pop(0)
            # Get the course codes
            course_string = line[0]
            courses = []
            # If there are multiple course codes, separate them out
            while "/" in course_string:
                i = course_string.index("/")
                courses.append(course_string[0:i])
                course_string = course_string[i + 1:len(course_string)]
            courses.append(course_string)
            line.pop(0)

            # Now the line is of the format:
            # [SECTiONS IN VARIOUS FORMATS, BUILDING, ROOM, DAY OF WEEK, MONTH, DAY OF MONTH, '@', START TIME, '-', END TIME, GRADES DUE]

            # Start at the end of the line - this is because we don't know how many entries the SECTIONS will be in since doc is formatted inconsistently

            # End time
            time2 = line[len(line) - 1]
            line.pop(len(line) - 1)
            line.pop(len(line) - 1)

            # Start time
            time1 = line[len(line) - 1]
            line.pop(len(line) - 1)
            line.pop(len(line) - 1)

            # Day of month
            day = line[len(line) - 1]
            line.pop(len(line) - 1)

            # Month
            month = line[len(line) - 1]
            line.pop(len(line) - 1)

            # Day of week
            weekday = line[len(line) - 1].replace(",", '')
            line.pop(len(line) - 1)

            # Room
            room = line[len(line) - 1]
            line.pop(len(line) - 1)

            # Building
            building = line[len(line) - 1]
            line.pop(len(line) - 1)

            # Everything left is the sections
            # Get the sections from the remainder and fix some formatting (take out of parens and remove commas and ampersands)
            sections = [x.replace(",", "").replace("(", "").replace(")", "") for x in line if x != ',' and x != '&']
            # If an entry is info for all sections of a class, write that and skip the rest
            all = False
            for section in sections:
                if "ALL" in section:
                    start_time, end_time = handle_times(time1, time2, day, month, year)
                    db_lines.append([season, year, major, course, None, start_time, end_time, building, room])
                    all = True
            if all:
                continue
            fixed_sections = []
            # Create seperate section entries for all sections within a range ([01-05] becomes [01,02,03,04,05])
            for section in sections:
                if '-' in section:
                    num1 = int(section[:section.index("-")])
                    num2 = int(section[section.index("-") + 1:])
                    sections.remove(section)
                    for i in range(num1, num2 + 1):
                        fixed_sections.append(i)
                else:
                    fixed_sections.append(int(section))
            sections = fixed_sections
            # Adds all the entries into the array
            for section in sections:
                for course in courses:
                    start_time, end_time = handle_times(time1, time2, day, month, year)
                    db_lines.append([season, year, major, course, int(section), start_time, end_time, building, room])
    return db_lines


# In[34]:


def display_and_write_csv(db_lines):
    # Place into pandas dateframe (not needed but useful for testing & makes writing to csv easier
    df = pd.DataFrame(columns=('Season', 'Year', 'Major', 'Course', 'Section', 'Start', 'End', 'Building', 'Room_Number'))
    for i in range(len(db_lines)):
        df.loc[i] = db_lines[i]
    # standardize datetimes
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])    
    if debug_mode:
        pd.set_option('display.max_rows', 500)
        display(df)
    # write to output csv
    df.to_csv('out.csv')


# In[35]:


db_lines = parser()
display_and_write_csv(db_lines)

