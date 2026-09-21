from common.request_util import RequestUtil

class LoginApi:
    def __init__(self):
        self.req = RequestUtil()

    def login(self, username, password):
        return self.req.request(
            'POST', '/admin/login',
            json={"username": username, "password": password}
        )