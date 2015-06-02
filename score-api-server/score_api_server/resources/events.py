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


class Events(restful.Resource):

    def get(self):
        request_json = request.json
        print(request_json)
        result = g.cc.events.get("e568e805-43c2-4565-b03b-189b6f31fed9")
        if len(result) == 2:
            r = result[0]
            r.append(result[1])
            return r
        else:
            return []
