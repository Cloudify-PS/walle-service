# Copyright (c) 2015 VMware. All rights reserved

from flask.ext import restful
from flask import g
from flask_restful_swagger import swagger

from score_api_server.common import util

from cloudify_rest_client import exceptions

logger = util.setup_logging(__name__)


class Events(restful.Resource):

    def get_events(self, json):
        try:
            logger.info("Seeking for events by execution-id: %s",
                        json['execution_id'])
            result = g.cc.events.get(json['execution_id'],
                                     json.get('from', 0),
                                     json.get('size', 100),
                                     json.get('include_logs', False))
            logger.info("Cloudify events: {0}.".format(str(result)))
            for event in result[0]:
                if event['context']['workflow_id'].startswith('score'):
                    event['context']['workflow_id'] = (
                        event['context']['workflow_id'][5:])
                event['context'] = util.remove_org_prefix(
                    event['context']
                )
            if len(result) == 2:
                r = result[0]
                r.append(result[1])
                return self._filter_messages(r)
            else:
                return []
        except exceptions.CloudifyClientError as e:
            logger.error(str(e))
            return util.make_response_from_exception(e)

    def _filter_messages(self, events):
        scoreinstall = 'scoreinstall'
        scoreuninstall = 'scoreuninstall'
        for event in events:
            if isinstance(event, dict):
                text_message = event['message']['text']
                if scoreinstall in text_message:
                    text_message = event['message']['text'].replace(
                        scoreinstall, 'install')
                elif scoreuninstall in text_message:
                    text_message = event['message']['text'].replace(
                        scoreuninstall, 'uninstall')
                event['message']['text'] = text_message
        return events

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
    @util.validate_json(
        {"type": "object",
         "properties": {
             "execution_id": {"type": "string", "minLength": 1},
             "from": {"type": "integer", "minimum": 0},
             "size": {"type": "integer", "minimum": 1},
             "include_logs": {"type": "boolean"}
         },
         "required": ["execution_id"]}
    )
    def get(self, json):
        logger.debug("Entering Events.get method.")
        result = self.get_events(json)
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
    @util.validate_json(
        {"type": "object",
         "properties": {
             "execution_id": {"type": "string", "minLength": 1},
             "from": {"type": "integer", "minimum": 0},
             "size": {"type": "integer", "minimum": 1},
             "include_logs": {"type": "boolean"}
         },
         "required": ["execution_id"]}
    )
    def post(self, json):
        logger.debug("Entering Events.post method.")
        result = self.get_events(json)
        logger.debug("Done. Exiting Events.post method.")
        return result
