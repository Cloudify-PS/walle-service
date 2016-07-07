
from flask.ext import restful
from flask_restful_swagger import swagger

from walle_api_server.common import util
from walle_api_server.resources import responses

logger = util.setup_logging(__name__)


class Endpoints(restful.Resource):

    @swagger.operation(
        nickname="getEndpoints",
        notes="Return full list of registered service urls, "
              "does't have any parameters.",
    )
    def get(self):
        logger.info("Listing all endpoint urls.")

        from walle_api_server.common import manage_limits

        status, value = manage_limits.endpoint_list()
        return [u.to_dict() for u in value]

    @swagger.operation(
        responseClass=responses.Endpoint,
        nickname="registerEndpoint",
        notes="Register new endpoint in system.",
        parameters=[{'name': 'endpoint_url',
                     'description': 'Endpoint Url',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'type',
                     'description': 'Enpoint type(openstack, vcloud)',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'version',
                     'description': 'Service version',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'description',
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
             "endpoint_url": {"type": "string", "minLength": 1},
             "type": {"type": "string", "minLength": 1},
             "version": {"type": ["string", "null"]},
             "description": {"type": ["string", "null"]},
         },
         "required": ["endpoint_url", "type"]}
    )
    def post(self, json):
        logger.info("Update endpoint.")

        from walle_api_server.common import manage_limits
        status, value = manage_limits.endpoint_add(
            json['endpoint_url'], json['type'],
            json['version'], json['description'])

        if status:
            return value.to_dict()
        else:
            return value


class EndpointsId(restful.Resource):
    @swagger.operation(
        nickname="DeleteEndpoint",
        notes="Delete endpoint url from system.",
        parameters=[{'name': 'id',
                     'description': 'Endpoint Url ID',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'}]
    )
    def delete(self, id):
        logger.info("Delete  endpoint url.")

        from walle_api_server.common import manage_limits
        _, value = manage_limits.endpoint_delete_id(id)

        return value

class Tenants(restful.Resource):
    @swagger.operation(
        nickname="getTenants",
        notes="Return full list of registered tenants with relation to "
              "cloudify manager.",
    )
    def get(self):
        logger.info("Listing all tenants.")

        from walle_api_server.common import manage_limits

        _, tenants = manage_limits.tenant_list()
        return [l.to_dict() for l in tenants]

    @swagger.operation(
        responseClass=responses.Tenant,
        nickname="RegisterTenant",
        notes="Add relation tenant to cloudify manager and endpoint",
        parameters=[{'name': 'endpoint_url',
                     'description': 'Endpoint Url',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'type',
                     'description': 'Enpoint type(openstack, vcloud)',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'tenant_name',
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
                    {'name': 'description',
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
             "endpoint_url": {"type": "string", "minLength": 1},
             "type": {"type": "string", "minLength": 1},
             "tenant_name": {"type": "string", "minLength": 1},
             "cloudify_host": {"type": "string", "minLength": 1},
             "cloudify_port": {"type": "string", "minLength": 1},
             "description": {"type": ["string", "null"]},
         },
         "required": ["endpoint_url", "type", "tenant_name", "cloudify_host",
                      "cloudify_port"]}
    )
    def post(self, json):
        logger.info("Create tenant.")
        from walle_api_server.common import manage_limits

        status, value = manage_limits.tenant_add(
            json['endpoint_url'], json['type'], json['tenant_name'],
            json['cloudify_host'], json['cloudify_port'],
            json['description']
        )
        if status:
            return value.to_dict()
        else:
            return value

    @swagger.operation(
        responseClass=responses.Tenant,
        nickname="UpdateTenant",
        notes="Update tenant.",
        parameters=[{'name': 'id',
                     'description': 'Tenant id',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'endpoint_url',
                     'description': 'Endpoint Url',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'type',
                     'description': 'Enpoint type(openstack, vcloud)',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'tenant_name',
                     'description': 'Tenant name',
                     'required': False,
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
                    {'name': 'description',
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
             "id": {"type": "string", "minLength": 1},
             "endpoint_url": {"type": ["string", "null"]},
             "type": {"type": ["string", "null"]},
             "tenant_name": {"type": ["string", "null"]},
             "cloudify_host": {"type": ["string", "null"]},
             "cloudify_port": {"type": ["string", "null"]},
             "description": {"type": ["string", "null"]},
         },
         "required": ["id"]}
    )
    def put(self, json):
        logger.info("Update keystore_url.")

        from walle_api_server.common import manage_limits

        status, value = manage_limits.tenant_update(**json)
        if status:
            return value.to_dict()
        else:
            return value


class TenantsId(restful.Resource):
    @swagger.operation(
        nickname="deleteTenant",
        notes="Delete tenant.",
        parameters=[{'name': 'id',
                     'description': 'Tenant id',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'}]
    )
    def delete(self, id):
        logger.info("Delete tenant.")

        from walle_api_server.common import manage_limits

        _, value = manage_limits.tenant_delete(id)
        return value


class Limits(restful.Resource):

    @swagger.operation(
        nickname="getLimits",
        notes="Return full list of limits.",
    )
    def get(self):
        logger.info("Listing all limits.")

        from walle_api_server.common import manage_limits

        _, limits = manage_limits.limit_list()
        return [l.to_dict() for l in limits]

    @swagger.operation(
        responseClass=responses.Limit,
        nickname="RegisterLimit",
        notes="Add relation tenant to cloudify manager and endpoint",
        parameters=[{'name': 'endpoint_url',
                     'description': 'Endpoint Url',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'type',
                     'description': 'Enpoint type(openstack, vcloud)',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'tenant_name',
                     'description': 'Tenant name',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'hard',
                     'description': 'hard limit',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'soft',
                     'description': 'soft limit',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'integer',
                     'paramType': 'body'},
                    {'name': 'limit_type',
                     'description': 'Limit type',
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
             "endpoint_url": {"type": "string", "minLength": 1},
             "type": {"type": "string", "minLength": 1},
             "tenant_name": {"type": "string", "minLength": 1},
             "soft": {"type": "string", "minLength": 1},
             "hard": {"type": "string", "minLength": 1},
             "limit_type": {"type": "string", "minLength": 1},
         },
         "required": ["endpoint_url", "type", "tenant_name", "hard",
                      "soft", "limit_type"]}
    )
    def post(self, json):
        logger.info("Create limit.")
        from walle_api_server.common import manage_limits

        status, value = manage_limits.limit_add(
            json['endpoint_url'], json['type'], json['tenant_name'],
            json['limit_type'], json['soft'],
            json['hard']
        )
        if status:
            return value.to_dict()
        else:
            return value

    @swagger.operation(
        responseClass=responses.Limit,
        nickname="UpdateLimit",
        notes="Update limit.",
        parameters=[{'name': 'id',
                     'description': 'Limit id',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'hard',
                     'description': 'hard limit',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'soft',
                     'description': 'soft limit',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'integer',
                     'paramType': 'body'},
                    {'name': 'limit_type',
                     'description': 'Limit type',
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
             "id": {"type": "string", "minLength": 1},
             "hard": {"type": ["string", "null"]},
             "soft": {"type": ["string", "null"]},
             "limit_type": {"type": ["string", "null"]},
         },
         "required": ["id"]}
    )
    def put(self, json):
        logger.info("Update limit.")

        from walle_api_server.common import manage_limits

        status, value = manage_limits.limit_update(**json)
        if status:
            return value.to_dict()
        else:
            return value


class LimitsId(restful.Resource):
    @swagger.operation(
        nickname="deleteTenantLimit",
        notes="Delete quota limits for tenant.",
        parameters=[{'name': 'id',
                     'description': 'Tenant Limit id',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'}]
    )
    def delete(self, id):
        logger.info("Delete limit.")
        from walle_api_server.common import manage_limits

        _, value = manage_limits.limit_delete(id)
        return value

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
