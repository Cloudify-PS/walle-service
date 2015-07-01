# Copyright (c) 2015 VMware. All rights reserved

from flask.ext import restful
from flask import request, g
from flask.ext.restful import reqparse
from score_api_server.common import util

parser = reqparse.RequestParser()
parser.add_argument('deployment_id', type=str, help='Deployment ID')


class Executions(restful.Resource):

    def get(self):
        args = parser.parse_args()
        deployment_id = util.add_org_prefix(args['deployment_id'])
        executions = g.cc.executions.list(deployment_id=deployment_id)
        return executions

    def post(self):
        deployment_id = util.add_org_prefix(request.json.get('deployment_id'))
        workflow_id = request.json.get('workflow_id')
        result = g.cc.executions.start(deployment_id, workflow_id)
        return result

    def put(self):
        execution_id = request.json.get('execution_id')
        force = request.json.get('force')
        result = g.cc.executions.cancel(execution_id, force)
        return result
