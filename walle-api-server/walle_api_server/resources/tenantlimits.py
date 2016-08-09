
from flask.ext import restful
from flask_restful_swagger import swagger

from walle_api_server.common import util
from walle_api_server.common import service_limit
from walle_api_server.resources import responses

logger = util.setup_logging(__name__)


class Limits(restful.Resource):

    @swagger.operation(
        nickname="getLimits",
        notes="Return full list of limits.",
    )
    def get(self):
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted
        logger.info("Listing all limits.")

        _, limits = manage_limits.limit_list()
        return [l.to_dict() for l in limits]

    @swagger.operation(
        responseClass=responses.Limit,
        nickname="RegisterLimit",
        notes="Add limit for tenant",
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
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Create limit.")

        status, value = manage_limits.limit_add(
            json['endpoint_url'], json['type'], json['tenant_name'],
            json['limit_type'], json['soft'],
            json['hard']
        )
        return service_limit.general_response_todict(status, value)

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
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Update limit.")

        status, value = manage_limits.limit_update(**json)
        return service_limit.general_response_todict(status, value)


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
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Delete limit.")

        _, value = manage_limits.limit_delete(id)
        return value
