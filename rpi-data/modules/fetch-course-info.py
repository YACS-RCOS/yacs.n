import requests as req
import threading
import unicodedata
import re
from threading import Lock
from io import StringIO
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree

catalog_id = 20 # 2019-2020 course catalog
chunk_size = 200 # max number of course ids per GET request
acalog_api_key = "3eef8a28f26fb2bcc514e6f1938929a1f9317628"

COURSE_DETAIL_TIMEOUT = 120.00 # seconds

allow_for_extension_regex = re.compile("(<catalog.*?>)|(<\/catalog>)|(<\?xml.*?\?>)")
prolog_and_root_ele_regex = re.compile("^(?P<prolog><\?xml.*?\?>)\s*(?P<root><catalog.*?>)")

def dwrite_obj(obj):
    with open("temp-xml.xml", "w") as file:
        file.write(obj.__str__())

# todo: - [ ] try to use <fields>...</fields> to get all possible fields and map <course> to these.
#       they'll just be that internal name like 'acalog-field-814'. Not sure if there's a good
#       and easy way to have a dynamic key name to properly represent the data.. Might just be easier to use static names
#       - [ ] need to add to requirements.txt or if virtualenv is ever set up, lxml, requests(? not sure if standard)
#       - [ ] need to dynamically fetch catalog id
#       - [ ] documentation??
#       - [ ] get rid of remaining part using beautifulsoup?

class acalog_client():
    def __init__(self, api_key):
        self.search_endpoint = "http://rpi.apis.acalog.com/v2/search/courses"
        self.course_detail_endpoint = "http://rpi.apis.acalog.com/v2/content?options[full]=1&method=getItems&type=courses"
        self.api_key = api_key
        self.api_response_format = "xml"
        self._lock = Lock()
        self._course_details_xml_strs = []
        self._xml_prolog = ""
        self._catalog_root = ""

    def _clean_utf(self, string):
        return unicodedata.normalize("NFKD", string)

    def _all_threads_joined(self, threads):
        for thread in threads:
            thread.join(COURSE_DETAIL_TIMEOUT)
            if (thread.is_alive()):
                return False
        return True

    def get_course_ids_xml(self):
        return req.get(f"{self.search_endpoint}?key={self.api_key}&format={self.api_response_format}&method=listing&catalog={catalog_id}&options[limit]=0").content

    def _get_course_details(self, id_params):
        course_details_xml_str = req.get(f"{self.course_detail_endpoint}&key={self.api_key}&format={self.api_response_format}&catalog=20&{id_params}").content.decode("utf8")
        with self._lock:
            # https://stackoverflow.com/questions/39119165/xml-what-does-that-question-mark-mean
            # Can only have one prolog per XML document in order for it to be well-formed.
            # Can also only have one root.
            # Don't see a reason to keep it as a bytestring, beautifulsoup
            # is eventually just going to convert it to utf8 anyway
            match = prolog_and_root_ele_regex.match(course_details_xml_str)
            self._xml_prolog = match.group("prolog")
            self._catalog_root = match.group("root")
            self._course_details_xml_strs.append(allow_for_extension_regex.sub("", course_details_xml_str))


    def _course_xml_ids_to_url_params(self, all_ids_xml):
        only_ids = SoupStrainer("id")
        id_tags = BeautifulSoup(all_ids_xml, "xml", parse_only=only_ids).find_all("id")
        return [f"ids[]={id_xml.text}" for id_xml in id_tags]

    def get_all_courses_xml(self, course_ids_url_params):
        course_count = len(course_ids_url_params)
        id_chunks = [course_ids_url_params[i:i+chunk_size] for i in range(0, course_count, chunk_size)]
        chunk_count = len(id_chunks)
        courses_xml = ""
        thread_jobs = []
        for id_chunk in id_chunks:
            query_param_chunk = "&".join(id_chunk)
            fetch_course_details_job = threading.Thread(target=self._get_course_details, args=[query_param_chunk], daemon=False)
            thread_jobs.append(fetch_course_details_job)
            fetch_course_details_job.start()
        # Wait until all jobs are finished
        while True:
            if self._all_threads_joined(thread_jobs):
                break
        courses_xml = self._xml_prolog + self._catalog_root + "".join(self._course_details_xml_strs) + "</catalog>"
        return courses_xml

    def _get_all_courses(self, courses_xml_str):
        tree = etree.parse(StringIO(courses_xml_str))
        # https://stackoverflow.com/a/4256011/8088388
        course_content_xml = tree.getroot().xpath("//*[local-name() = 'course']/*[local-name() = 'content']")
        courses = []
        for raw_course in course_content_xml:
            # The description <field> can have multiple children tags, so get all text nodes.
            # One example of this is ARCH 4870 - Sonics Research Lab 1, catalog 20, courseid 38592
            description_xml = raw_course.xpath("*[local-name() = 'field'][@type='acalog-field-471']")
            name_xml = raw_course.xpath("*[local-name() = 'name']")
            # If it has the description, it will be the correct schema of a course object.
            # For some reason the course tag is used for not actual courses. Fun.
            if (description_xml and name_xml):
                description = " ".join(description_xml[0].xpath(".//text()"))
                name = name_xml[0].text
                # https://stackoverflow.com/a/34669482/8088388
                courses.append({"description": self._clean_utf(description), "full_name": self._clean_utf(name)})
        return courses

    def get_all_courses(self):
        ids_xml = self.get_course_ids_xml()
        ids = self._course_xml_ids_to_url_params(ids_xml)
        courses_xml_str = self.get_all_courses_xml(ids)
        return self._get_all_courses(courses_xml_str)

def main():
    c = acalog_client(acalog_api_key)
    courses = c.get_all_courses()
    # print(len(courses))
    print(courses[0])

if __name__ == "__main__":
    main()