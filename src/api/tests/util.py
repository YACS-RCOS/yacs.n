import requests

class Client():
    def __init__(self):
        self.URL = "http://0.0.0.0:5000"
        self.session = requests.Session()

<<<<<<< HEAD
    def get(self, endpoint, params=None, json=None, data=None, headers=None):
        return requests.get(self.URL + endpoint, params=params, json=json, data=data, headers = headers)
=======

    def get(self, endpoint, params=None, json=None, data=None, headers=None):
        return requests.get(self.URL + endpoint, params=params, json=json, data=data, headers = headers)

>>>>>>> 18dd7be0c1905c8103715fa9f1621e2b76dbff2f

    def post(self, endpoint, params=None, json=None, data=None, files=None):
        return self.session.post(self.URL + endpoint, params=params, json=json, files=files, data=data)

    def put(self, endpoint, params=None, json=None, data=None, headers=None):
        return self.session.put(self.URL + endpoint, params=params, json=json, data=data, headers = headers)

    def delete(self, endpoint, params=None, json=None, data=None):
        return self.session.delete(self.URL + endpoint, params=params, json=json, data=data)
