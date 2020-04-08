#!/usr/bin/env python
# coding: utf-8

# In[1]:
from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag

import datetime
import os
import requests
import pandas as pd
import json
from fetch_course_info import acalog_client

SEMESTER_NAME = "FALL 2020"

# In[13]:

source_url = "https://sis.rpi.edu/reg/zfs202009.htm"

response = requests.get(source_url)
content = response.text

# Removes all divs to avoid bad parsing
cont = content.split("\n")
cont = filter(lambda x: not "div" in x, cont)
content = "\n".join(cont)

# In[14]:

soup = BeautifulSoup(content, 'html.parser')

# In[15]:

tables = soup.findChildren('table')
genInfo = soup.findChildren('center')

# In[20]:

def get_course_titles(my_row):
    res = []
    for child in my_row.children:
        if isinstance(child, NavigableString):
            continue
        if isinstance(child, Tag):
            children = child.findChildren("span", recursive=True)
            for child_2 in children:
                res.append(child_2.contents[0])
    return res

def get_course_row(my_row):
    res = []
    for item in my_row.findChildren('td'):
        children = item.findChildren('span')
        #print(children)
        if(len(children) == 0):
            res.append(None)
        else:
            res.append(children[0].contents[0])

    res.pop()
    return res

def parse_time(time_string):
    time = time_string.split('-')
    time[0] = time[0].strip()
    time[1] = time[1].split(',')
    time[1][0] = time[1][0].strip()
    time[1][1] = time[1][1].strip()
    time[0] = time[0] + ' ' + time[1][1]
    time[1] = time[1][0] + ' ' + time[1][1]
    time[0] = datetime.datetime.strptime(time[0], '%B %d %Y')
    time[1] = datetime.datetime.strptime(time[1], '%B %d %Y')
    time[0] = str(time[0].date())
    time[1] = str(time[1].date())
    return time

# In[25]:

data = []
schls = []
current_course_section = ''
current_course_title = ''
current_course_hrs = ''
current_course_max_enroll = ''
current_course_enrolled = ''
current_course_remained = ''

time_raw = genInfo[0].findChildren('h3', recursive=True)[1].findChildren('span')[0].contents[0]
time = parse_time(time_raw)

for gens in genInfo:
    # time = gens.findChildren(['h3'])
    schools = gens.findChildren('h4', recursive=False)
    # print(time[1].findChildren('span')[0].contents[0])

    for school in schools:
        schls.append(school.findChildren('span')[0].contents[0])

for i in range(len(tables)):
    table = tables[i]
    #print(table)
    #print("----------------------------------------------")
    rows = table.findChildren(['tr'])
    # print(rows)
    if i == 0:
        titles = get_course_titles(rows[1])

    for row in rows[2:]:
        info = get_course_row(row)
        if(len(info) < 12):
            continue

        elif(len(info) == 12):
        	info.insert(9, 'TBA')

        if not info[0]:
            prev = data[-1]
            info[0] = prev[0]
            info[1] = prev[1]

            info[3] = prev[3]

            info[10] = prev[9]
            info[11] = prev[10]
            info[12] = prev[11]

        info.append(schls[i])
        info.append(time[0])
        info.append(time[1])
        info.append(SEMESTER_NAME)

        if(info[5]):
            info[5] = info[5].replace(' ', '').strip()
        if(info[6]):
            info[6] = info[6].replace(' ', '').strip()
        if(info[7]):
            info[7] = info[7].replace(' ', '').strip()


        if(info[7]):
            if info[7][-2:] == 'AM':
                info[6] += 'AM'
            else:
                col = info[6].find(':')
                if (int(info[6][:col]) < 8) or (int(info[6][:col]) == 12):
                    info[6] += "PM"
                else:
                    info[6] += "AM"
        else:
            info[6] = info[7] = None

        if 'TBA' in info[9]:
        	info[9] = None

        info.pop(4)
        data.append(info)


# In[27]:


df = pd.DataFrame(data, columns=[
    'course_genertal_info',
    'course_name',
    'course_type',
    'course_credit_hours',
    'course_days_of_the_week',
    'course_start_time',
    'course_end_time',
    'course_instructor',
    'course_location',
    'course_max_enroll',
    'course_enrolled',
    'course_remained',
    'course_department',
    'course_start_date',
    'course_end_date',
    'semester'
])

# df.course_days_of_the_week = df.course_days_of_the_week.apply(
#     lambda x: x.replace(' ', '').strip())
# df.course_start_time = df.course_start_time.apply(
#     lambda x: x.replace(' ', '').strip())
# df.course_end_time = df.course_end_time.apply(
#     lambda x: x.replace(' ', '').strip())

# In[28]:


df = df.assign(course_crn=df.course_genertal_info.apply(lambda x: x[:5]))
df = df.assign(
    course_department=df.course_genertal_info.apply(lambda x: x[6:10]))
df = df.assign(course_level=df.course_genertal_info.apply(lambda x: x[11:15]))
df = df.assign(course_section=df.course_genertal_info.apply(lambda x: x[16:]))


# In[29]:


df = df.drop(columns=['course_genertal_info'])

# In[30]:

headers = os.environ.get('HEADERS', 'True')

headers = (headers == 'True')

destination = os.environ.get('DEST', 'out.csv')


# In[ ]:

df = df.assign(short_name=lambda row: row['course_department']+"-"+row['course_level'])

# In[]:

course_info_dict = {}
with open(r"C:\\Users\\corey\\Documents\\Programming\\OpenSource\\yacs.n\\rpi-data\\modules\\courses20.json", "r") as file:
    course_info_dict = json.load(file)
ci_df = pd.DataFrame(course_info_dict)
joined = df.join(other=ci_df.set_index("short_name"), how="left", on=["short_name"])

# df.to_csv(destination, header=headers, index=False)

# %%
