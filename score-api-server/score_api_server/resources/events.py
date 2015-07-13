# Copyright (c) 2015 VMware. All rights reserved

from flask.ext import restful
from flask import request, g, make_response

from score_api_server.common import util

from cloudify_rest_client import exceptions

logger = util.setup_logging(__name__)


class Events(restful.Resource):

    def get(self):
        logger.debug("Entering Events.get method.")
        try:
            request_json = request.json
            logger.info("Seeking for events by execution-id: %s",
                        request_json.get('execution_id'))
            result = g.cc.events.get(request_json.get('execution_id'),
                                     request_json.get('from'),
                                     request_json.get('size'),
                                     request_json.get('include_logs'))
            logger.debug("Done. Exiting Events.get method.")
            if len(result) == 2:
                r = result[0]
                r.append(result[1])
                return r
            else:
                return []
        except exceptions.CloudifyClientError as e:
            logger.error(str(e))
            return make_response(str(e), e.status_code)
