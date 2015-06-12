# Copyright (c) 2015 VMware. All rights reserved

from flask.ext import restful
from flask import request, g
from flask.ext.restful import reqparse
from score_api_server.common import util


parser = reqparse.RequestParser()
parser.add_argument('deployment_id', type=str, help='Deployment ID')


class Executions(restful.Resource):

    def get(self, execution_id=None):
        args = parser.parse_args()
        deployment_id = args['deployment_id']
        deployment_id = util.add_org_prefix(deployment_id)
        executions = g.cc.executions.list(deployment_id=deployment_id)
        return executions

    def post(self):
        request_json = request.json
        deployment_id = request_json.get('deployment_id')
        deployment_id = util.add_org_prefix(deployment_id)
        workflow_id = request_json.get('workflow_id')
        result = g.cc.executions.start(deployment_id, workflow_id)
        return result
