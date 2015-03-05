import os
import tempfile
import tarfile
import shutil
import json

from flask.ext import restful
from flask import request, abort, g

from cloudify_rest_client.client import CloudifyClient
from cloudify_rest_client.blueprints import BlueprintsClient
from cloudify_rest_client.deployments import DeploymentsClient

class Deployments(restful.Resource):

    def get(self, deployment_id=None):
        if deployment_id is not None:
            if not deployment_id.startswith(g.org_id+'_'): 
                return None
            return g.cc.deployments.get(deployment_id)
        else:
            deployments = g.cc.deployments.list()
            result = []
            for deployment in deployments:
                if deployment.id.startswith(g.org_id+'_'): result.append(deployment)
            return result
            
    def delete(self, deployment_id):
        assert deployment_id and deployment_id.startswith(g.org_id+'_')
        deployment = g.cc.deployments.delete(deployment_id)
        return deployment
        
    def put(self, deployment_id):
        assert deployment_id and deployment_id.startswith(g.org_id+'_')
        request_json = request.json
        blueprint_id = request_json.get('blueprint_id')
        assert blueprint_id and blueprint_id.startswith(g.org_id+'_')
        inputs = json.loads(request_json.get('inputs'))
        deployment = g.cc.deployments.create(blueprint_id, deployment_id, inputs=inputs)
        return deployment

