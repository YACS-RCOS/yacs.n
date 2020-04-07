import requests as req
import threading
import unicodedata
import re
# Needed for branch reset regex
import regex
import json
from time import time
from threading import Lock
from io import StringIO
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree

catalog_id = 20 # 2019-2020 course catalog
chunk_size = 200 # max number of course ids per GET request
acalog_api_key = "3eef8a28f26fb2bcc514e6f1938929a1f9317628"
dev_output_files = True

ACALOG_COURSE_FIELDS = {
    "Department": "acalog-field-486",
    "Level": "acalog-field-488",
    "FullName": "acalog-field-490",
    "Description": "acalog-field-471",
    "PreCoReqs": "acalog-field-473",
    "OfferFrequency": "acalog-field-475",
    "CrossListed": "acalog-field-478",
    "Graded": "acalog-field-480",
    "CreditHours": "acalog-field-482",
    "ContactLectureLabHours": "acalog-field-484",
}
COURSE_DETAIL_TIMEOUT = 120.00 # seconds

allow_for_extension_regex = re.compile("(<catalog.*?>)|(<\/catalog>)|(<\?xml.*?\?>)")
prolog_and_root_ele_regex = re.compile("^(?P<prolog><\?xml.*?\?>)?\s*(?P<root><catalog.*?>)")

# group the most specific regex patterns first, then the more general ones for last
# goal is to capture classes that are loosely of the form "Prerequisites: [CAPTURE COURSE LISTINGS TEXT]",
# but does not capture classes explicitly stated to be corequisites. Tries to remove
# periods, trailing and leading space.
explicit_prereqs_include_syntax_regex = "(?:^\s*Prerequisites? include:?\s?(.*))"
explicit_prereqs_preference_syntax_regex = "(?:^\s*Prerequisites? preferences?:?\s*(.*))"
explicit_prereqs_or_coreqs_syntax_regex = "(?:^\s*Prerequisites? or Corequisites?:?\s?(.*))"
explicit_prereqs_before_coreqs_syntax_regex = "(?:^\s*Prerequisites?.*?:\s?(.*?(?=\W*Coreq)))"
explicit_prereqs_sequence_syntax_regex = "(?:^\s*Prerequisites?:?\s*(.*(?=[\. ;,])))"
# https://stackoverflow.com/questions/406230/regular-expression-to-match-a-line-that-doesnt-contain-a-word
# doesn't contain a "prerequisites:" sort of string
# if there is leading space then it will be captured. I'm not sure how to not capture it.
implicit_prereqs_syntax_regex = "(^((?!(Corequisite)).)*$)"
implicit_prereqs_before_coreqs_syntax_regex = "(?:^\s*(.*?(?=\W*Coreq)))"
full_prereqs_regex = "|".join([
    explicit_prereqs_include_syntax_regex,
    explicit_prereqs_preference_syntax_regex,
    explicit_prereqs_or_coreqs_syntax_regex,
    explicit_prereqs_before_coreqs_syntax_regex,
    explicit_prereqs_sequence_syntax_regex,
    implicit_prereqs_syntax_regex,
    implicit_prereqs_before_coreqs_syntax_regex
])
# https://stackoverflow.com/a/44463324/8088388
branch_reset_prereqs_regex = regex.compile(f"(?|{full_prereqs_regex})", flags=regex.IGNORECASE|regex.DOTALL)
coreqs_regex = re.compile("Prerequisites?:?\s*(?P<prereqs>.*?(?=\W*Coreq))", flags=regex.IGNORECASE)

def dwrite_obj(obj, name):
    with open(name, "w") as file:
        file.write(obj.__str__())

def dwrite_text(text, name):
    with open(name, "w") as file:
        file.write(text)

def dwrite_utf8_file(text, name):
    with open(name, "w", encoding='utf-8') as file:
        file.write(text)

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

    # https://stackoverflow.com/a/34669482/8088388
    def _clean_utf(self, string):
        # unicodedata.normalize("NFKD", string)
        # Format the unicode string into its normalized combined version,
        # and get rid of unprintable characters
        return unicodedata.normalize("NFKC", string)
        # return unicodedata.normalize("NFKC", string).encode('cp1252','replace').decode('cp1252')

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
            if (match is None):
                raise Error("XML document is missing prolog and root. Invalid.")
            self._xml_prolog = match.group("prolog") if match.group("prolog") is not None else '<?xml version="1.0"?>'
            if match.group("root") is None:
                raise Error("XML document is missing root element. Invalid.")
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

    def _extract_prereqs(self, precoreqs):
        match = regex.search(branch_reset_prereqs_regex, precoreqs)
        if (match is not None):
            if len(match.groups()) > 0:
                return match.groups()[0]
        return ""

    def _get_all_courses(self, courses_xml_str):
        parser = etree.XMLParser(encoding="utf-8")
        tree = etree.parse(StringIO(courses_xml_str), parser=parser)
        # https://stackoverflow.com/a/4256011/8088388
        course_content_xml = tree.getroot().xpath("//*[local-name() = 'course']/*[local-name() = 'content']")
        courses = []
        for raw_course in course_content_xml:
            # The description <field> can have multiple children tags, so get all text nodes.
            # One example of this is ARCH 4870 - Sonics Research Lab 1, catalog 20, courseid 38592
            course_id = re.search("(?P<id>\d+)$", raw_course.getparent().attrib["id"]).group("id")
            description_xml = raw_course.xpath("*[local-name() = 'field'][@type='acalog-field-471']")
            name_xml = raw_course.xpath("*[local-name() = 'name']")
            # If it has the description, it will be the correct schema of a course object.
            # For some reason the course tag is used for not actual courses. Fun.
            if (description_xml and name_xml):
                description = " ".join(description_xml[0].xpath(".//text()"))
                precoreqs = " ".join(raw_course.xpath(f"*[local-name() = 'field'][@type='{ACALOG_COURSE_FIELDS['PreCoReqs']}']//text()"))
                prereqs = self._extract_prereqs(precoreqs)
                name = name_xml[0].text
                courses.append(
                        {
                            "id": course_id,
                            "full_name": self._clean_utf(name),
                            "description": self._clean_utf(description).encode("utf8").decode("utf8"),
                            "prerequisites": self._clean_utf(prereqs),
                            "raw_precoreqs": self._clean_utf(precoreqs)
                        }
                )
        return courses

    def get_all_courses(self):
        ids_xml = self.get_course_ids_xml()
        ids = self._course_xml_ids_to_url_params(ids_xml)
        courses_xml_str = self.get_all_courses_xml(ids)
        if dev_output_files:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(StringIO(courses_xml_str), parser)
            tree.write("courses20.xml", pretty_print=True)
        return self._get_all_courses(courses_xml_str)

def main():
    c = acalog_client(acalog_api_key)
    courses = c.get_all_courses()
    if dev_output_files:
        dwrite_utf8_file(json.dumps(courses, indent=4), "courses20.json")

if __name__ == "__main__":
    main()