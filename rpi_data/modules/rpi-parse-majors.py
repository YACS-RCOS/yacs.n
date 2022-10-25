#!/usr/bin/env python
# coding: utf-8
# %%
import json
import pandas as pd
import os
from fetch_catalog_course_info import acalog_client as AcalogClient
from fetch_sis_course_info import sis_client as SisClient
from add_school_column import add_school_column

acalog_api_key = "3eef8a28f26fb2bcc514e6f1938929a1f9317628"

acalog_client = AcalogClient(acalog_api_key)

acalog_course_info_df = pd.DataFrame(acalog_client.get_all_courses())

destination = os.environ.get('DEST', 'out.json')

with open(destination.replace(".csv", ".json"), "w") as file:
    json.dump(acalog_client.get_all_majors(), file)