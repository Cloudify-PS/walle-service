# Copyright (c) 2015 VMware. All rights reserved

from flask.ext import restful
from flask import request, g
from flask.ext.restful import reqparse

parser = reqparse.RequestParser()


class Events(restful.Resource):

    def get(self):
        request_json = request.json
        print(request_json)
        result = g.cc.events.get("e568e805-43c2-4565-b03b-189b6f31fed9")
        if len(result) == 2:
            r = result[0]
            r.append(result[1])
            return r
        else:
            return []
