import yaml
import pandas as pd
import requests
import re

from typing import Dict
from bs4 import BeautifulSoup

RPI_FACULTY_PATH = "https://faculty.rpi.edu"
PROF_EMAIL_MAPPING_PATH = RPI_FACULTY_PATH + "/data/peoplesearch"

class ProfEmailMapping:
    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping
    
    @classmethod
    def get_emails(cls, path: str):

        r = requests.get(path).json()

        mapping: Dict[str, str] = {}

        for prof in r['nodes']:
            site = RPI_FACULTY_PATH + prof['node']['Path']
            soup = BeautifulSoup(requests.get(site).text, 'lxml')

            #better way to do this?
            try:
                mapping[prof] = soup.find_all(href=re.compile('mailto'))[0].get_text()
            except:
                mapping[prof] = ""

        return cls(mapping)


def add_prof_emails(df: pd.DataFrame, path = PROF_EMAIL_MAPPING_PATH):
    prof_email_mapping = ProfEmailMapping.get_emails(path)