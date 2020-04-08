#!/usr/bin/env python
# coding: utf-8
# %%
import json
import pandas as pd
import os
from fetch_catalog_course_info import acalog_client as AcalogClient
from fetch_sis_course_info import sis_client as SisClient

semester_name = "FALL 2020" #os.environ['SEMESTER']
source_url = "https://sis.rpi.edu/reg/zfs202009.htm" #os.environ.get('SOURCE_URL')
acalog_api_key = "3eef8a28f26fb2bcc514e6f1938929a1f9317628"

sis_client = SisClient(semester_name, source_url)
# todo, can't use. need to refactor vars in file to be class members
acalog_client = AcalogClient(acalog_api_key)

courses_df = sis_client.run()

course_info_dict = {}
with open(r"C:\\Users\\corey\\Documents\\Programming\\OpenSource\\yacs.n\\rpi-data\\modules\\courses20.json", "r") as file:
    course_info_dict = json.load(file)
ci_df = pd.DataFrame(course_info_dict)
# ci_df.to_csv("catalog20.csv", header=True, index=False)
ci_df = ci_df.drop(columns=['id'])
courses_df = courses_df.assign(short_name=lambda row: row['course_department']+"-"+row['course_level'])

joined = courses_df.join(other=ci_df.set_index("short_name"), how="left", on=["short_name"])

headers = os.environ.get('HEADERS', 'True')
headers = (headers == 'True')
destination = os.environ.get('DEST', 'out.csv')
joined.to_csv("catalog_sis_merged.csv", header=headers, index=False)
# courses_df.to_csv(destination, header=headers, index=False)
