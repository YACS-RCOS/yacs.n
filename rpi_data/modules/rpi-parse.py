#!/usr/bin/env python
# coding: utf-8
# %%
import json
import pandas as pd
import os
from fetch_catalog_course_info import acalog_client as AcalogClient
from fetch_sis_course_info import sis_client as SisClient
from add_school_column import add_school_column
from add_prof_emails import add_prof_emails

semester_name = os.environ['SEMESTER']
source_url = os.environ.get('SOURCE_URL')
acalog_api_key = "3eef8a28f26fb2bcc514e6f1938929a1f9317628"

sis_client = SisClient(semester_name, source_url)
acalog_client = AcalogClient(acalog_api_key)

sis_course_info_df = sis_client.run()
acalog_course_info_df = pd.DataFrame(acalog_client.get_all_courses())

# Will join on this temp field
sis_course_info_df = sis_course_info_df.assign(short_name=lambda row: row['course_department']+"-"+row['course_level'])

combined_course_info_df = sis_course_info_df.join(other=acalog_course_info_df.set_index("short_name"), how="left", on=["short_name"])
combined_course_info_df = combined_course_info_df.drop(columns=['department', 'level'])
combined_course_info_df = add_school_column(combined_course_info_df)
combined_course_info_df = add_prof_emails(combined_course_info_df)

headers = os.environ.get('HEADERS', 'True')
headers = (headers == 'True')
destination = os.environ.get('DEST', 'out.csv')
combined_course_info_df.to_csv(destination, header=headers, index=False)
