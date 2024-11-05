import sys
import requests


csv_loc = sys.argv1[1]

url = 'http://localhost:8080/api/bulkCourseUpload'

content = open(csv_loc, 'r').read()

response = requests.post(url,data=content)
print(response.text)