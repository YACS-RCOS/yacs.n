import requests as req
import threading
import unicodedata
import re
from io import StringIO
from bs4 import BeautifulSoup, SoupStrainer

catalog_id = 20 # 2019-2020 course catalog
chunk_size = 200 # max number of course ids per GET request
acalog_api_key = "3eef8a28f26fb2bcc514e6f1938929a1f9317628"

ending_catalog_regex = re.compile("</catalog>$")
allow_for_extension_regex = re.compile("(<catalog.*?>)|(<\/catalog>)|(<\?xml.*?\?>)")
closed_for_extension_regex = re.compile("(<catalog.*?>)|(<\?xml.*?\?>)")

def dwrite_obj(obj):
    with open("temp-xml.xml", "w") as file:
        file.write(obj.__str__())

class acalog_client():
    def __init__(self, api_key):
        self.search_endpoint = "http://rpi.apis.acalog.com/v2/search/courses"
        self.course_detail_endpoint = "http://rpi.apis.acalog.com/v2/content?options[full]=1&method=getItems&type=courses"
        self.api_key = api_key
        self.api_response_format = "xml"

    def _clean_utf(self, string):
        return unicodedata.normalize("NFKD", string)

    def _get_course_ids(self):
        return req.get(f"{self.search_endpoint}?key={self.api_key}&format={self.api_response_format}&method=listing&catalog={catalog_id}&options[limit]=0")

    def _get_course_details(self, id_params):
        return req.get(f"{self.course_detail_endpoint}&key={self.api_key}&format={self.api_response_format}&catalog=20&{id_params}")

    def _course_xml_ids_to_url_params(self, ids):
        only_ids = SoupStrainer("id")
        all_ids_xml_resp = ids
        id_tags = BeautifulSoup(all_ids_xml_resp.content, "xml", parse_only=only_ids).find_all("id")
        return [f"ids[]={id_xml.text}" for id_xml in id_tags]

    def get_all_courses_xml(self, course_ids_url_params):
        course_count = len(course_ids_url_params)
        id_chunks = [course_ids_url_params[i:i+chunk_size] for i in range(0, course_count, chunk_size)]
        chunk_count = len(id_chunks)
        courses_xml_chunks = []
        for i, id_chunk in enumerate(id_chunks):
            query_param_chunk = "&".join(id_chunk)
            resp = self._get_course_details(query_param_chunk)
            # if first get rid of ending </catalog>
            # else get rid of prolog and <catalog> and </catalog>
            if (i != 0 and i != chunk_count - 1):
                # https://stackoverflow.com/questions/39119165/xml-what-does-that-question-mark-mean
                # Can only have one prolog per XML document in order for it to be well-formed.
                courses_xml_chunks.append(allow_for_extension_regex.sub("", resp.content.decode("utf8")))
            elif (i == chunk_count - 1):
                courses_xml_chunks.append(closed_for_extension_regex.sub("", resp.content.decode("utf8")))
            else:
                # Don't see a reason to keep it as a bytestring, beautifulsoup
                # is eventually just going to convert it to utf8 anyway
                courses_xml_chunks.append(ending_catalog_regex.sub("", resp.content.decode("utf8")))
        return courses_xml_chunks

    def _get_all_courses(self, courses_xml_chunks):
        courses = []
        only_courses = SoupStrainer("courses")
        merged = "".join(courses_xml_chunks)
        # dwrite_obj(merged)
        bs = BeautifulSoup(merged, "xml", parse_only=only_courses)
        raw_courses_xml = bs.find_all("course")
        for raw_course in raw_courses_xml:
            content = raw_course.find("content")
            description = content.find(type="acalog-field-471")
            # If it has the description, it will be the correct schema of a course object.
            # For some reason the course tag is used for not actual courses. Fun.
            if (description):
                # https://stackoverflow.com/a/34669482/8088388
                courses.append({"description": self._clean_utf(content.find(type="acalog-field-471").text), "full_name": self._clean_utf(content.find("name").text)})
        return courses

    def get_all_courses(self):
        ids_xml = self._get_course_ids()
        ids = self._course_xml_ids_to_url_params(ids_xml)
        course_xml_chunks = self.get_all_courses_xml(ids)
        # Should be 10 <catalog>..</catalog> tags where each has <= chunk (200) courses.
        # dwrite_obj(course_xml_chunks)
        return self._get_all_courses(course_xml_chunks)

def main():
    c = acalog_client(acalog_api_key)
    courses = c.get_all_courses()
    print(len(courses))

if __name__ == "__main__":
    main()