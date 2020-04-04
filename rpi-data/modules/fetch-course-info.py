import requests as req
import asyncio
import unicodedata
from io import StringIO
from bs4 import BeautifulSoup, SoupStrainer

acalog_api_key = "3eef8a28f26fb2bcc514e6f1938929a1f9317628"
api_response_format = "xml"
catalog_id = 20 # 2019-2020 course catalog
chunk_size = 200 # max number of course ids per GET request

acalog_search_endpoint = "http://rpi.apis.acalog.com/v2/search/courses"
acalog_course_detail_endpoint = "http://rpi.apis.acalog.com/v2/content?options[full]=1&method=getItems&type=courses"

def clean_utf(string):
    return unicodedata.normalize("NFKD", string)

async def request_all_course_ids():
    return req.get(f"{acalog_search_endpoint}?key={acalog_api_key}&format={api_response_format}&method=listing&catalog={catalog_id}&options[limit]=0")

async def request_course_details(id_params):
    return req.get(f"{acalog_course_detail_endpoint}&key={acalog_api_key}&format={api_response_format}&catalog=20&{id_params}")

async def get_all_course_ids_as_url_params():
    only_ids = SoupStrainer("id")
    all_ids_xml_resp = await request_all_course_ids()
    id_tags = BeautifulSoup(all_ids_xml_resp.content, "xml", parse_only=only_ids).find_all("id")
    return [f"ids[]={id_xml.text}" for id_xml in id_tags]

async def get_all_courses_xml(course_ids_url_params):
    course_count = len(course_ids_url_params)
    id_chunks = [course_ids_url_params[i:i+chunk_size] for i in range(0, course_count, chunk_size)]
    courses_xml_chunks = []
    for id_chunk in id_chunks:
        query_param_chunk = "&".join(id_chunk)
        resp = await request_course_details(query_param_chunk)
        courses_xml_chunks.append(resp.content)
    return courses_xml_chunks

async def get_all_courses(courses_xml_chunks):
    courses = []
    for course_chunk in courses_xml_chunks:
        bs = BeautifulSoup(course_chunk, "xml")
        root = bs.find("catalog")
        raw_courses_xml = root.find_all("courses")

        for raw_course in raw_courses_xml:
            content = raw_course.find("content")
            department = content.find("prefix").text
            level = content.find("code").text
            title = content.find("name").text
            # https://stackoverflow.com/a/34669482/8088388
            courses.append({"description": clean_utf(content.find(type="acalog-field-471").text), "full_name": clean_utf(content.find("name").text)})
    return courses

async def main():
    course_id_params = await get_all_course_ids_as_url_params()
    courses_xml = await get_all_courses_xml(course_id_params)
    courses = await get_all_courses(courses_xml)
    print(courses[0])

asyncio.run(main())