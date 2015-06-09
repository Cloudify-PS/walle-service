# Copyright (c) 2015 VMware. All rights reserved

from flask.ext import restful
from flask import request, g
from flask.ext.restful import reqparse

parser = reqparse.RequestParser()


class Events(restful.Resource):

    def get(self):
        request_json = request.json
        result = g.cc.events.get(request_json.get('execution_id'),
                                 request_json.get('from'),
                                 request_json.get('size'),
                                 request_json.get('include_logs'))
        if len(result) == 2:
            r = result[0]
            r.append(result[1])
            return r
        else:
            return []
