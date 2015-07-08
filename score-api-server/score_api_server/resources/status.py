# Copyright (c) 2015 VMware. All rights reserved

import flask

import score_api_server

from flask import g, make_response
from flask.ext import restful

from cloudify_rest_client import exceptions

app = flask.Flask(__name__)


class Status(restful.Resource):

    def get(self):
        app.logger.debug("Entering Status.get method.")
        try:
            app.logger.info("Checking Score version.")
            score_version = score_api_server.get_version()
            app.logger.info("Checking Cloudify manager version.")
            manager_version = g.cc.manager.get_version()
            app.logger.info("Checking Cloudify manager status.")
            manager_status = g.cc.manager.get_status()
            app.logger.debug("Done. Exiting Status.get method.")
            return {"score_version": score_version,
                    "manager_version": manager_version["version"],
                    "manager_status": manager_status["status"]}
        except (Exception, exceptions.CloudifyClientError) as e:
            app.logger.error(str(e))
            return make_response(str(e), 400 if not isinstance(
                e, exceptions.CloudifyClientError) else e.status_code)
