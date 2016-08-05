from flask.ext import restful
from flask import request


class Ui(restful.Resource):

    def get(self):
        return {"name": "walle-io", "version": "3.4.0"}


class Logined(restful.Resource):

    def get(self):
        result = False
        username = ""
        if request.headers.get('x-openstack-authorization'):
            result = True
            username = "user"
        return {"username": username, "result": result}


class Latest(restful.Resource):

    def get(self):
        return True


class Logout(restful.Resource):

    def post(self):
        return True
