# Copyright (c) 2015 VMware. All rights reserved

import json

from flask.ext import restful
from flask import request, g
from score_api_server.common import util


class Deployments(restful.Resource):

    def get(self, deployment_id=None):
        if deployment_id is not None:
            result = g.cc.deployments.get(util.add_org_prefix(deployment_id))
            return util.remove_org_prefix(result)
        else:
            deployments = g.cc.deployments.list()
            result = []
            for deployment in deployments:
                if deployment.id.startswith(g.org_id + '_'):
                    result.append(util.remove_org_prefix(deployment))
            return result

    def delete(self, deployment_id):
        result = g.cc.deployments.delete(util.add_org_prefix(deployment_id))
        return result

    def put(self, deployment_id):
        blueprint_id = request.json.get('blueprint_id')
        inputs = json.loads(request.json.get('inputs'))
        deployment = g.cc.deployments.create(
            util.add_org_prefix(blueprint_id),
            util.add_org_prefix(deployment_id),
            inputs=inputs)
        return deployment
