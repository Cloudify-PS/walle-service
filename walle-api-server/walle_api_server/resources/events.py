# Copyright (c) 2015 VMware. All rights reserved

from flask.ext import restful
from flask import g, request
from flask_restful_swagger import swagger

from walle_api_server.common import util

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
                if event['context']['workflow_id'].startswith('walle'):
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
        walleinstall = 'walleinstall'
        walleuninstall = 'walleuninstall'
        for event in events:
            if isinstance(event, dict):
                text_message = event['message']['text']
                if walleinstall in text_message:
                    text_message = event['message']['text'].replace(
                        walleinstall, 'install')
                elif walleuninstall in text_message:
                    text_message = event['message']['text'].replace(
                        walleuninstall, 'uninstall')
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
    def get(self):
        logger.debug("Entering Events.get method.")
        args = request.args
        if 'blueprint_id' not in args and 'deployment_id' not in args:
            return {"items": [],
                    "metadata": {
                        "pagination": {
                            "offset": 0,
                            "size": 0,
                            "total": 0}}}
        result = g.proxy.get(request)
        logger.debug("Done. Exiting Events.get method.")
        items = []
        for item in result['items']:
            if item['context'].get('blueprint_id') and \
               item['context'].get('blueprint_id').startswith(g.tenant_id):
                context = item['context']
                item['context'] = util.remove_org_prefix(context)
            items.append(item)
        result['items'] = items
        return result
