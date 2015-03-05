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

parser = reqparse.RequestParser()
parser.add_argument('deployment_id', type=str, help='Deployment ID')

class Executions(restful.Resource):

    def get(self, execution_id=None):
        args = parser.parse_args()
        deployment_id = args['deployment_id']
        assert deployment_id and deployment_id.startswith(g.org_id+'_')
        executions = g.cc.executions.list(deployment_id=deployment_id)
        return executions
        
    def post(self):
        request_json = request.json
        deployment_id = request_json.get('deployment_id')
        workflow_id = request_json.get('workflow_id')
        assert deployment_id and deployment_id.startswith(g.org_id+'_')
        assert workflow_id
        result = g.cc.executions.start(deployment_id, workflow_id)
        return result
        