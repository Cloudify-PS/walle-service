# Copyright (c) 2015 VMware. All rights reserved

from flask import g, make_response
from flask.ext import restful
# from flask_restful_swagger import swagger

from pyvcloud.vcloudair import VCA

from score_api_server.common import util
# from score_api_server.resources import responses


logger = util.setup_logging(__name__)


class VCAInstances(restful.Resource):

    def _try_to_login(self):
        vca = VCA(None, None, None, None)
        result = vca.login(token=g.token)
        if not result:
            raise Exception(
                "Unable to log in using session token")
        return vca

    def _do_instance_get(self):
        try:
            vca = self._try_to_login()
            logger.info("User instances: {0}".format(
                str(vca.instances)))
            return vca.instances
        except Exception as e:
            logger.error(str(e))
            return make_response(str(e), 401)

    def get(self):
        #return self._do_instance_get()
        return make_response("Not implemented.", 405)

