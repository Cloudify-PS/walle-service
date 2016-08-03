
from flask.ext import restful
from flask_restful_swagger import swagger

from walle_api_server.common import util
from walle_api_server.common import service_limit
from walle_api_server.resources import responses

logger = util.setup_logging(__name__)


class Tenants(restful.Resource):
    @swagger.operation(
        nickname="getTenants",
        notes="Return full list of registered tenants with relation to "
              "cloudify manager.",
    )
    def get(self):
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Listing all tenants.")

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
                    {'name': 'create',
                     'description': 'Create on VIM',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'body'},
                    {'name': 'admin_endpoint',
                     'description': 'Additional params for create on VIM',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'json',
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
             "create": {"type": "string", "minLength": 1},
             "admin_endpoint": {"type": ["string", "null"]},
             "description": {"type": ["string", "null"]},
         },
         "required": ["endpoint_url", "type", "tenant_name", "cloudify_host",
                      "cloudify_port"]}
    )
    def post(self, json):
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Create tenant.")

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
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Update tenant.")

        status, value = manage_limits.tenant_update(**json)
        if status:
            return value.to_dict()
        else:
            return value

    @swagger.operation(
        nickname="DeleteTenant",
        notes="Remove tenant from walle",
        parameters=[{'name': 'endpoint_url',
                     'description': 'Endpoint Url',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'},
                    {'name': 'type',
                     'description': 'Enpoint type(openstack, vcloud)',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'},
                    {'name': 'tenant_name',
                     'description': 'Tenant name',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'},
                    {'name': 'delete',
                     'description': 'Delete on VIM',
                     'required': True,
                     'allowMultiple': False,
                     'dataType': 'string',
                     'paramType': 'path'},
                    {'name': 'admin_endpoint',
                     'description': 'Additional params for create on VIM',
                     'required': False,
                     'allowMultiple': False,
                     'dataType': 'json',
                     'paramType': 'path'}],
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
             "delete": {"type": "string", "minLength": 1},
             "admin_endpoint": {"type": ["string", "null"]},
         },
         "required": ["endpoint_url", "type", "tenant_name", "cloudify_host",
                      "cloudify_port"]}
    )
    def delete(self):
        # from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Delete tenant.")

        # Not implemented, receive tenant + endpoint url and admin endpoint
        pass


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
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Delete tenant.")

        _, value = manage_limits.tenant_delete(id)
        return value
