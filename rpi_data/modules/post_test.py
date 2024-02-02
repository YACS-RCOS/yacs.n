import requests
import os

url = os.environ.get('yacs_url')
url = "http://localhost:5000"
api_location = url + "/api/bulkCourseUpload"
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def csvUpload(fileName):
    headers = {'Content-Type': 'text/csv'}
    endpath = os.path.join(__location__, fileName)
    endpath = os.path.dirname(os.path.dirname(endpath)) + "\\" + fileName
    print(endpath)
    data = {'name': "file", 'filename': fileName}
    file = {'filename': open(endpath, 'rb')}
    r = requests.post(api_location, headers=headers, data=data, files=file)
    print(r.reason, r.status_code)

if __name__ == "__main__":
    csvUpload("spring-2021.csv")