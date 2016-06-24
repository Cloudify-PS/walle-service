
from flask.ext import restful
from flask_restful_swagger import swagger

from walle_api_server.common import util
from walle_api_server.resources import responses

logger = util.setup_logging(__name__)


class ServiceUrls(restful.Resource):

    @swagger.operation(
        nickname="getServiceUrls",
        notes="Return full list of registered service urls, "
              "does't have any parameters.",
    )
    def get(self):
        logger.debug("Entering ServiceUrls.get method.")
        logger.info("Listing all service_url.")

        from walle_api_server.db import models
        keystore_url = models.AllowedServiceUrl.list()
        return [u.to_dict() for u in keystore_url]

    @swagger.operation(
        responseClass=responses.ServiceUrl,
        nickname="RegisterServiceUrl",
        notes="Register new service url in system.",
        parameters=[{'name': 'service_url',
                     'description': 'Service Url',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'tenant',
                     'description': 'Tenant name',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'info',
                     'description': 'Descrition for service url',
                     'required': False,
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
             "service_url": {"type": "string", "minLength": 1},
             "tenant": {"type": "string", "minLength": 1},
             "info": {"type": ["string", "null"]},
         },
         "required": ["service_url", "tenant"]}
    )
    def post(self, json):
        logger.debug("Entering ServiceUrls.post method.")
        logger.info("Update keystore_url.")
        from walle_api_server.db import models
        service = models.AllowedServiceUrl.find_by(
            service_url=json['service_url'],
            tenant=json['tenant'])
        if service:
            return "Sorry, Already exist"
        url = models.AllowedServiceUrl(
            json['service_url'], json['tenant'], info=json['info']
        )
        return url.to_dict()


class ServiceUrlsId(restful.Resource):
    @swagger.operation(
        nickname="DeleteServiceUrl",
        notes="Delete service url from system.",
        parameters=[{'name': 'id',
                     'description': 'Service Url ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'}]
    )
    def delete(self, id):
        logger.debug("Entering ServiceUrlsId.delete method.")
        logger.info("Delete service_url.")
        from walle_api_server.db import models
        service = models.AllowedServiceUrl.find_by(id=id)
        if service:
            service.delete()
            return "OK"
        else:
            return "ERROR: keystore_url not found"


class ServiceUrlLimits(restful.Resource):
    @swagger.operation(
        nickname="getServiceUrlLimits",
        notes="Return full list of registered service urls "
              "with limits.",
    )
    def get(self):
        logger.debug("Entering OrgIdLimitss.get method.")
        logger.info("Listing all keystore_url_limit.")
        from walle_api_server.db import models
        limits = models.ServiceUrlToCloudifyAssociationWithLimits.list()
        return [l.to_dict() for l in limits]

    @swagger.operation(
        responseClass=responses.ServiceUrlLimit,
        nickname="RegisterServiceUrlLimit",
        notes="Set quota limits for service url.",
        parameters=[{'name': 'service_url',
                     'description': 'Service Url',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'tenant',
                     'description': 'Tenant name',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'cloudify_host',
                     'description': 'Cloudify host ip/name',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'cloudify_port',
                     'description': 'Cloudify port',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'integer',
                     'paramType': 'body'},
                    {'name': 'deployment_limits',
                     'description': 'deployment limits',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'integer',
                     'paramType': 'body'}],
        consumes=[
            "application/json"
        ]
    )
    @util.validate_json(
        {"type": "object",
         "properties": {
             "service_url": {"type": "string", "minLength": 1},
             "tenant": {"type": "string", "minLength": 1},
             "cloudify_host": {"type": "string", "minLength": 1},
             "cloudify_port": {"type": "string", "minLength": 1},
             "deployment_limits": {"type": "string", "minLength": 1},
         },
         "required": ["service_url", "tenant", "cloudify_host",
                      "cloudify_port", "deployment_limits"]}
    )
    def post(self, json):
        logger.debug("Entering ServiceUrlLimits.post method.")
        logger.info("Create org_id_limits.")
        from walle_api_server.db import models
        service = models.AllowedServiceUrl.find_by(
            service_url=json['service_url'],
            tenant=json['tenant'])
        if not service:
            return "ERROR: No such Service url."
        limit = models.ServiceUrlToCloudifyAssociationWithLimits.find_by(
            serviceurl_id=service.id)
        if limit:
            return "Sorry, Already exist"

        limit = models.ServiceUrlToCloudifyAssociationWithLimits(
            service.id,
            json['cloudify_host'],
            json['cloudify_port'],
            json['deployment_limits'],
        )
        return limit.to_dict()

    @swagger.operation(
        responseClass=responses.ServiceUrlLimit,
        nickname="UpdateServiceUrlLimit",
        notes="Update quota limits for service url.",
        parameters=[{'name': 'id',
                     'description': 'Service Url Limit id',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'cloudify_host',
                     'description': 'Cloudify host ip/name',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'cloudify_port',
                     'description': 'Cloudify port',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'integer',
                     'paramType': 'body'},
                    {'name': 'deployment_limits',
                     'description': 'deployment limits',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'integer',
                     'paramType': 'body'},
                    {'name': 'number_of_deployments',
                     'description': 'current number of deployments',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'integer',
                     'paramType': 'body'}],
        consumes=[
            "application/json"
        ]
    )
    @util.validate_json(
        {"type": "object",
         "properties": {
             "id": {"type": "string", "minLength": 1},
             "cloudify_host": {"type": ["string", "null"]},
             "cloudify_port": {"type": ["string", "null"]},
             "deployment_limits": {"type": ["string", "null"]},
             "number_of_deployments": {"type": ["string", "null"]},
         },
         "required": ["id"]}
    )
    def put(self, json):
        logger.debug("Entering ServiceUrlLimits.put method.")
        logger.info("Update keystore_url.")
        from walle_api_server.db import models
        update_json = {}
        limit_id = json["id"]

        keys = ["cloudify_host", "cloudify_port",
                "deployment_limits", "number_of_deployments"]

        for key in keys:
            if json.get(key):
                update_json.update({key: json.get(key)})

        if not limit_id:
            return "ERROR: ID required."

        limit = models.ServiceUrlToCloudifyAssociationWithLimits.find_by(
            id=limit_id)
        if not limit:
            return "No such keystore_url limit entity."
        else:
            limit.update(**update_json)
            updated_limit = (
                models.ServiceUrlToCloudifyAssociationWithLimits.find_by(
                    id=limit_id))
            return updated_limit.to_dict()


class ServiceUrlLimitsId(restful.Resource):
    @swagger.operation(
        nickname="deleteServiceUrlLimit",
        notes="Delete quota limits for service url.",
        parameters=[{'name': 'id',
                     'description': 'Service Url Limit id',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'}]
    )
    def delete(self, id):
        logger.debug("Entering ServiceUrlLimitsId.delete method.")
        logger.info("Delete keystore_url_limit.")
        from walle_api_server.db import models
        limit = models.ServiceUrlToCloudifyAssociationWithLimits.find_by(
            id=id
        )
        if not limit:
            return "ERROR: No such keystore_url_limit entity."
        else:
            limit.delete()
            return "OK"


class ApprovedPlugins(restful.Resource):
    @swagger.operation(
        nickname="getApprovedPluginList",
        notes="Return full list of approved plugins.",
    )
    def get(self):
        logger.debug("Entering ApprovedPlugins.get method.")
        logger.info("Listing all keystore_url.")

        from walle_api_server.db import models
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
        plugin = models.ApprovedPlugins.find_by(id=id)
        if plugin:
            plugin.delete()
            return "Deleted"
        else:
            return "ERROR: No such plugin name entity."
