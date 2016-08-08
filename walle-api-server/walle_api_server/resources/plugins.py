
from flask.ext import restful
from flask_restful_swagger import swagger

from walle_api_server.common import util
from walle_api_server.common import service_limit
from walle_api_server.resources import responses

logger = util.setup_logging(__name__)


class ApprovedPlugins(restful.Resource):
    @swagger.operation(
        nickname="getApprovedPluginList",
        notes="Return full list of approved plugins.",
    )
    def get(self):
        logger.debug("Entering ApprovedPlugins.get method.")
        logger.info("Listing all keystore_url.")

        from walle_api_server.db import models

        restricted = service_limit.cant_edit_plugins()
        if restricted:
            return restricted

        plugins = models.ApprovedPlugins.list()
        return [u.to_dict() for u in plugins]

    @swagger.operation(
        responseClass=responses.ApprovedPlugin,
        nickname="addPluginToApproved",
        notes="add plugin to approved.",
        parameters=[{'name': 'name',
                     'description': 'plugin name',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'source',
                     'description': 'plugin url',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'type',
                     'description': 'plugin type',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'}],
        consumes=[
            "application/json"
        ]
    )
    @util.validate_json(
        {"type": "object",
         "properties": {
             "name": {"type": "string"},
             "source": {"type": "string"},
             "type": {"type": "string"},
         },
         "required": ["name", "source", "type"]}
    )
    def post(self, json):
        logger.debug("Entering ApprovedPlugins.post method.")
        logger.info("Update keystore_url.")
        from walle_api_server.db import models

        restricted = service_limit.cant_edit_plugins()
        if restricted:
            return restricted

        plugin = models.ApprovedPlugins(json["name"],
                                        json["source"], json["type"])
        return plugin.to_dict()


class ApprovedPluginsFromFile(restful.Resource):
    @swagger.operation(
        nickname="addPluginsToApproved",
        notes="add plugins to approved.",
        parameters=[{'name': 'from_file',
                     'description': 'File with list of plugins',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'}],
        consumes=[
            "application/json"
        ]
    )
    @util.validate_json(
        {"type": "object",
         "properties": {
             "from_file": {"type": "array"},
         },
         "required": ["from_file"]}
    )
    def post(self, json):
        logger.debug("Entering ApprovedPluginsFromFile.post method.")
        logger.info("Update keystore_url.")
        from walle_api_server.db import models

        restricted = service_limit.cant_edit_plugins()
        if restricted:
            return restricted

        for name, source, type in json['from_file']:
            models.ApprovedPlugins(name, source, type)
        return "Registered {} plugins".format(len(json['from_file']))


class ApprovedPluginsId(restful.Resource):
    @swagger.operation(
        nickname="seleteApprovedPlugin",
        notes="Delete approved plugin record.",
        parameters=[{'name': 'id',
                     'description': 'Approved plugin id',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'}]
    )
    def delete(self, name):
        logger.debug("Entering ApprovedPlugins.delete method.")
        logger.info("Delete plugin.")
        from walle_api_server.db import models

        restricted = service_limit.cant_edit_plugins()
        if restricted:
            return restricted

        plugin = models.ApprovedPlugins.find_by(id=id)
        if plugin:
            plugin.delete()
            return "Deleted"
        else:
            return "ERROR: No such plugin name entity."
