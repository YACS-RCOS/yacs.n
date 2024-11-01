import requests
import base64
import os

url = os.environ.get('yacs_url')
url = "http://localhost:5000"
api_location = url + "/api/bulkCourseUpload"
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


def csvUpload(fileName):
    endpath = os.path.join(__location__, fileName)
    endpath = os.path.dirname(os.path.dirname(endpath)) + "\\" + fileName
    print(endpath)
    uploadFile = {'file': open(endpath, 'rb')}
    data = {'isPubliclyVisible': 'on'}

    r = requests.post(api_location, files=uploadFile, data=data)
    print(r.reason, r.status_code)


if __name__ == "__main__":
    csvUpload("spring-2022.csv")
