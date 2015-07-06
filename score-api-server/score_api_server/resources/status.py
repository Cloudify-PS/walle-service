# Copyright (c) 2015 VMware. All rights reserved
from flask.ext import restful
from flask import g
import score_api_server


class Status(restful.Resource):

    def get(self):
        score_version = score_api_server.get_version()
        manager_version = g.cc.manager.get_version()
        manager_status = g.cc.manager.get_status()

        return {"score_version": score_version,
                "manager_version": manager_version["version"],
                "manager_status": manager_status["status"]}
