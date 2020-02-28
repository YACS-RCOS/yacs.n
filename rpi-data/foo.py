#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from bs4 import NavigableString,Tag


# In[13]:


import requests

response = requests.get('https://sis.rpi.edu/reg/zs20200502.htm')
content = response.text


# In[14]:


soup = BeautifulSoup(content, 'html.parser')


# In[15]:


tables = soup.findChildren('table')


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


# In[25]:


data = []
current_course_section = ''
current_course_title = ''
current_course_hrs = ''
current_course_max_enroll = ''
current_course_enrolled = ''
current_course_remained = ''


for table in tables[:]:
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
                current_course_remained
            ]
            data.append(clean_info)


# In[27]:


import pandas as pd 

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


df.to_csv('out.csv')


# In[ ]:




