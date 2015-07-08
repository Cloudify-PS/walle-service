# Copyright (c) 2015 VMware. All rights reserved

import score_api_server

from flask import g, make_response
from flask.ext import restful

from cloudify_rest_client import exceptions


class Status(restful.Resource):

    def get(self):
        try:
            score_version = score_api_server.get_version()
            manager_version = g.cc.manager.get_version()
            manager_status = g.cc.manager.get_status()

            return {"score_version": score_version,
                    "manager_version": manager_version["version"],
                    "manager_status": manager_status["status"]}
        except exceptions.CloudifyClientError as e:
            return make_response(str(e), e.status_code)
