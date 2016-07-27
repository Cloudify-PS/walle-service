# Copyright (c) 2015 VMware. All rights reserved

from flask.ext import restful
from flask import g, request

from walle_api_server.common import util


logger = util.setup_logging(__name__)


class Nodes(restful.Resource):

    def get(self):
        logger.debug("Entering Nodes.get method.")
        nodes = g.proxy.get(request)
        util.filter_response(nodes, "deployment_id")
        logger.debug("Done. Exiting Nodes.get method.")
        return nodes


class NodeInstances(restful.Resource):
    def get(self):
        logger.debug("Entering NodeInstances.get method.")
        instances = g.proxy.get(request)
        logger.debug("Done. Exiting NodeInstances.get method.")
        util.filter_response(instances, "deployment_id")
        return instances
