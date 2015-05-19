import os
import tempfile
import tarfile
import shutil
import json

from flask.ext import restful
from flask import request, abort, g
from flask.ext.restful import reqparse

from cloudify_rest_client.client import CloudifyClient
from cloudify_rest_client.blueprints import BlueprintsClient
from cloudify_rest_client.deployments import DeploymentsClient
from cloudify_rest_client.executions import ExecutionsClient
from cloudify_rest_client.events import EventsClient

parser = reqparse.RequestParser()

class Events(restful.Resource):

    def get(self):
        request_json = request.json
        print request_json
        result = g.cc.events.get("e568e805-43c2-4565-b03b-189b6f31fed9")
        if len(result) == 2:
            r = result[0]
            r.append(result[1])
            return r
        else:
            return []
