# Copyright (c) 2015 VMware. All rights reserved

from flask.ext import restful
from flask import request, g
from flask_restful_swagger import swagger

from score_api_server.common import util

from cloudify_rest_client import exceptions

logger = util.setup_logging(__name__)


class Events(restful.Resource):

    def get_events(self):
        try:
            request_json = request.json
            logger.info("Seeking for events by execution-id: %s",
                        request_json.get('execution_id'))
            result = g.cc.events.get(request_json.get('execution_id'),
                                     request_json.get('from'),
                                     request_json.get('size'),
                                     request_json.get('include_logs'))
            if len(result) == 2:
                r = result[0]
                r.append(result[1])
                return r
            else:
                return []
        except exceptions.CloudifyClientError as e:
            logger.error(str(e))
            return util.make_response_from_exception(e)

    @swagger.operation(
        nickname='events',
        notes='Returns a list of events.',
        parameters=[{'name': 'execution_id',
                     'description': 'Execution ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'from',
                     'description': 'Index of event',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'defaultValue': '0',
                     'paramType': 'body'},
                    {'name': 'size',
                     'description': 'Batch size',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'defaultValue': '100',
                     'paramType': 'body'},
                    {'name': 'include_logs',
                     'description': 'Include logs',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'boolean',
                     'defaultValue': False,
                     'paramType': 'body'}],
        consumes=['application/json']
    )
    def get(self):
        logger.debug("Entering Events.get method.")
        result = self.get_events()
        logger.debug("Done. Exiting Events.get method.")
        return result

    @swagger.operation(
        nickname='events',
        notes='Returns a list of events.',
        parameters=[{'name': 'execution_id',
                     'description': 'Execution ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'query'},
                    {'name': 'from_event',
                     'description': 'Index of event',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'defaultValue': '0',
                     'paramType': 'query'},
                    {'name': 'batch_size',
                     'description': 'Batch size',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'defaultValue': '100',
                     'paramType': 'query'},
                    {'name': 'include_logs',
                     'description': 'Include logs',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'boolean',
                     'defaultValue': False,
                     'paramType': 'query'}],
        consumes=['application/json']
    )
    def post(self):
        logger.debug("Entering Events.post method.")
        result = self.get_events()
        logger.debug("Done. Exiting Events.post method.")
        return result
