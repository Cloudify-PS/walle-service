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

from flask.ext import restful
from flask import request, g
from flask.ext.restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('deployment_id', type=str, help='Deployment ID')


class Executions(restful.Resource):

    def get(self, execution_id=None):
        args = parser.parse_args()
        deployment_id = args['deployment_id']
        executions = g.cc.executions.list(deployment_id=deployment_id)
        return executions

    def post(self):
        request_json = request.json
        deployment_id = request_json.get('deployment_id')
        workflow_id = request_json.get('workflow_id')
        result = g.cc.executions.start(deployment_id, workflow_id)
        return result
