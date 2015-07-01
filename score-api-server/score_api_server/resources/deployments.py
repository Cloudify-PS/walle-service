# Copyright (c) 2015 VMware. All rights reserved

import json

from flask.ext import restful
from flask import request, g, abort
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
        from score_api_server.common import org_limit
        result = g.cc.deployments.delete(util.add_org_prefix(deployment_id))
        # looks good decrement usage count
        if result:
            org_limit.decrement()
        return result

    def put(self, deployment_id):
        from score_api_server.common import org_limit
        request_json = request.json
        blueprint_id = request_json.get('blueprint_id')
        inputs = json.loads(request_json.get('inputs'))
        if not org_limit.increment():
            # overcommit
            abort(401)
        deployment = None
        try:
            deployment = g.cc.deployments.create(
                util.add_org_prefix(blueprint_id),
                util.add_org_prefix(deployment_id),
                inputs=inputs)
        finally:
            # something going wrong, try to return back
            if not deployment:
                org_limit.decrement()
        return deployment
