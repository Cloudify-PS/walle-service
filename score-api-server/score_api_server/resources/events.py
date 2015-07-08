# Copyright (c) 2015 VMware. All rights reserved

import flask

from flask.ext import restful
from flask import request, g, make_response
from flask.ext.restful import reqparse

from cloudify_rest_client import exceptions

app = flask.Flask(__name__)
parser = reqparse.RequestParser()


class Events(restful.Resource):

    def get(self):
        app.logger.debug("Entering Events.get method.")
        try:
            request_json = request.json
            app.logger.info("Seeking for events by execution-id: %s",
                            request_json.get('execution_id'))
            result = g.cc.events.get(request_json.get('execution_id'),
                                     request_json.get('from'),
                                     request_json.get('size'),
                                     request_json.get('include_logs'))
            app.logger.debug("Done. Exiting Events.get method.")
            if len(result) == 2:
                r = result[0]
                r.append(result[1])
                return r, 200
            else:
                return [], 200
        except exceptions.CloudifyClientError as e:
            app.logger.error(str(e))
            return make_response(str(e), e.status_code)
