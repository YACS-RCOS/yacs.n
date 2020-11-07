from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag

import datetime
import requests
import pandas as pd

class sis_client:
    def __init__(self, semester_name, source_url):
        self.SEMESTER_NAME = semester_name
        self.source_url = source_url

    def get_course_titles(self, my_row):
        res = []
        for child in my_row.children:
            if isinstance(child, NavigableString):
                continue
            if isinstance(child, Tag):
                children = child.findChildren("span", recursive=True)
                for child_2 in children:
                    res.append(child_2.contents[0])
        return res

    def get_course_row(self, my_row):
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

    def parse_time(self, time_string):
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

    def run(self):
        if not self.SEMESTER_NAME or not self.source_url:
            raise Error("Sis client requires semester name and source url")

        response = requests.get(self.source_url)
        content = response.text

        # Removes all divs to avoid bad parsing
        cont = content.split("\n")
        cont = filter(lambda x: not "div" in x, cont)
        content = "\n".join(cont)

        soup = BeautifulSoup(content, 'html.parser')

        tables = soup.findChildren('table')
        genInfo = soup.findChildren('center')

        data = []
        schls = []
        current_course_section = ''
        current_course_title = ''
        current_course_hrs = ''
        current_course_max_enroll = ''
        current_course_enrolled = ''
        current_course_remained = ''

        # NOTE: The Value 2, findChildren('h3', recursive=True)[2], 
        # May Change Semester To Semester Depending On # Lines Above/Below Each SIS Section. 
        raw_semester_start_end_data = genInfo[0].findChildren('h3', recursive=True)[2].findChildren('span')[0].contents[0]
        semester_start_end_data = self.parse_time(raw_semester_start_end_data)

        for gens in genInfo:
            schools = gens.findChildren('h4', recursive=False)
            for school in schools:
                schls.append(school.findChildren('span')[0].contents[0])

        for i, table in enumerate(tables):
            rows = table.findChildren(['tr'])
            if i == 0:
                titles = self.get_course_titles(rows[1])

            for row in rows[2:]:
                info = self.get_course_row(row)
                if(len(info) < 12):
                    continue

                info.pop(3) #pops unneeded data

                if(len(info) == 12):
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
                info.append(semester_start_end_data[0])
                info.append(semester_start_end_data[1])
                info.append(self.SEMESTER_NAME)

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

        df = df.assign(course_crn=df.course_genertal_info.apply(lambda x: x[:5]))
        df = df.assign(course_department=df.course_genertal_info.apply(lambda x: x[6:10]))
        df = df.assign(course_level=df.course_genertal_info.apply(lambda x: x[11:15]))
        df = df.assign(course_section=df.course_genertal_info.apply(lambda x: x[16:]))

        df = df.drop(columns=['course_genertal_info'])

        return df
