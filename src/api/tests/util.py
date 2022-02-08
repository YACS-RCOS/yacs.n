import requests

class Client():
    def __init__(self):
        self.URL = "http://0.0.0.0:5000"

    def get(self, endpoint, json=None):
        return requests.get(self.URL + endpoint, json=json)

    def post(self, endpoint, json=None):
        return requests.post(self.URL + endpoint, json=json)

    def put(self, endpoint, json=None):
        return requests.put(self.URL + endpoint, json=json)

    def delete(self, endpoint, json=None):
        return requests.delete(self.URL + endpoint, json=json)
