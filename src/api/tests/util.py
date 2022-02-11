import requests

class Client():
    def __init__(self):
        self.URL = "http://0.0.0.0:5000"

    def get(self, endpoint, params=None, json=None, data=None, headers=None):
        return requests.get(self.URL + endpoint, params=params, json=json, data=data, headers = headers)

    def post(self, endpoint, params=None, json=None, data=None, files=None):
        return requests.post(self.URL + endpoint, params=params, json=json, files=files, data=data)

    def put(self, endpoint, params=None, json=None, data=None):
        return requests.put(self.URL + endpoint, params=params, json=json, data=data)

    def delete(self, endpoint, params=None, json=None, data=None):
        return requests.delete(self.URL + endpoint, params=params, json=json, data=data)
