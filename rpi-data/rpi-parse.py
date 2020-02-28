#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from bs4 import NavigableString,Tag

import datetime
import os
import requests
import pandas as pd 



# In[13]:


source_url = os.environ.get('SOURCE_URL')
assert(source_url)

response = requests.get(source_url)
content = response.text


# In[14]:


soup = BeautifulSoup(content, 'html.parser')


# In[15]:


tables = soup.findChildren('table')

genInfo = soup.findChildren('center')


# In[20]:


def get_foo(my_row):
    res = []
    for child in my_row.children:
        if isinstance(child, NavigableString): 
            continue
        if isinstance(child, Tag): 
            children = child.findChildren("span" , recursive=False)
            for child_2 in children:
                res.append(child_2.contents[0])
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

time_raw = genInfo[0].findChildren('h3', recursive = False)[1].findChildren('span')[0].contents[0]
time = parse_time(time_raw)

for gens in genInfo:
    # time = gens.findChildren(['h3'])
    schools = gens.findChildren('h4', recursive = False);
    # print(time[1].findChildren('span')[0].contents[0])

    for school in schools:
        schls.append(school.findChildren('span')[0].contents[0])

for i in range(len(tables)):
    table = tables[i]
    rows = table.findChildren([ 'tr'])
    for row in rows[:]:
        info = get_foo(row)
        if len(info) == 11 : 
            current_course_section = info[0]
            current_course_title = info[1]
            current_course_hrs = info[3]
            current_course_max_enroll = info[8]
            current_course_enrolled = info[9]
            current_course_remained = info[10]
            info.append(schls[i])
            info.append(time[0])
            info.append(time[1])
            
            
            data.append(info)
            continue
        if len(info) == 5 :
            clean_info = [
                current_course_section,
                current_course_title,
                info[0], # Course type
                current_course_hrs,
                info[1],
                info[2],
                info[3],
                info[4],
                current_course_max_enroll,
                current_course_enrolled,
                current_course_remained,
                schls[i],
                time[0],
                time[1],
            ]
            data.append(clean_info)


# In[27]:


df = pd.DataFrame(data, columns =[
    'course_genertal_info', 
    'course_name',
    'course_type',
    'course_credit_hours',
    'course_days_of_the_week',
    'course_start_time',
    'course_end_time',
    'course_instructor',
    'course_max_enroll',
    'course_enrolled',
    'course_remained',
    'course_department',
    'course_start_date',
    'course_end_date',
    
]) 

df.course_days_of_the_week = df.course_days_of_the_week.apply(lambda x : x.replace(' ','').strip())
df.course_start_time = df.course_start_time.apply(lambda x : x.replace(' ','').strip())
df.course_end_time = df.course_end_time.apply(lambda x : x.replace(' ','').strip())


# In[28]:


df = df.assign(course_crn = df.course_genertal_info.apply(lambda x : x[:5]))
df = df.assign(course_department = df.course_genertal_info.apply(lambda x : x[6:10]))
df = df.assign(course_level = df.course_genertal_info.apply(lambda x : x[11:15]))
df = df.assign(course_section = df.course_genertal_info.apply(lambda x : x[16:]))


# In[29]:


df = df.drop(columns=['course_genertal_info'])


# In[30]:

headers = os.environ.get('HEADERS', 'True')

headers = (headers == 'True')

destination = os.environ.get('DEST', 'out.csv')

df.to_csv(destination, header = headers, index = False)


# In[ ]:




