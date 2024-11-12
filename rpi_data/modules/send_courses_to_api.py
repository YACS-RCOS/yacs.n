import sys
import requests

csv_loc = sys.argv[1]

url = 'http://localhost:8080/api/bulkCourseUpload'


content = {
        'isPubliclyVisible': (None, "on"),
        'file': (open(csv_loc, 'rb')),
    }

response = requests.post(url,files=content)
print(response.text)