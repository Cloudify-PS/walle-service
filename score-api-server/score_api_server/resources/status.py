# Copyright (c) 2015 VMware. All rights reserved

import score_api_server

from flask import g, make_response
from flask.ext import restful

from cloudify_rest_client import exceptions

from score_api_server.common import util

logger = util.setup_logging(__name__)


class Status(restful.Resource):

    def get(self):
        logger.debug("Entering Status.get method.")
        try:
            logger.info("Checking Score version.")
            score_version = score_api_server.get_version()
            logger.info("Checking Cloudify manager version.")
            manager_version = g.cc.manager.get_version()
            logger.info("Checking Cloudify manager status.")
            manager_status = g.cc.manager.get_status()
            logger.debug("Done. Exiting Status.get method.")
            return {"score_version": score_version,
                    "manager_version": manager_version["version"],
                    "manager_status": manager_status["status"]}
        except (Exception, exceptions.CloudifyClientError) as e:
            logger.error(str(e))
            return make_response(str(e), 400 if not isinstance(
                e, exceptions.CloudifyClientError) else e.status_code)
