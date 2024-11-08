import sys
import requests
csv_loc = sys.argv[1]

url = 'http://localhost:8080/api/bulkCourseUpload'

#content =
content = {
        'file': (open(csv_loc, 'rb').read()),
        'isPubliclyVisible': (None, "on"),
    }
response = requests.post(url,data=content)
print(response.text)

f = open("response.txt", "w+")
f.write(response.text)