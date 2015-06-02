# Copyright (c) 2015 VMware. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

import json

from flask.ext import restful
from flask import request, g


class Deployments(restful.Resource):

    def get(self, deployment_id=None):
        if deployment_id is not None:
            if not deployment_id.startswith(g.org_id + '_'):
                return None
            return g.cc.deployments.get(deployment_id)
        else:
            deployments = g.cc.deployments.list()
            result = []
            for deployment in deployments:
                if deployment.id.startswith(g.org_id + '_'):
                    result.append(deployment)
            return result

    def delete(self, deployment_id):
        return g.cc.deployments.delete(deployment_id)

    def put(self, deployment_id):
        request_json = request.json
        blueprint_id = request_json.get('blueprint_id')
        inputs = json.loads(request_json.get('inputs'))
        deployment = g.cc.deployments.create(
            blueprint_id, deployment_id, inputs=inputs)
        return deployment
