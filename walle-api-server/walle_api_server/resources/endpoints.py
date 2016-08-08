
from flask.ext import restful
from flask_restful_swagger import swagger

from walle_api_server.common import util
from walle_api_server.common import service_limit
from walle_api_server.resources import responses

logger = util.setup_logging(__name__)


class Endpoints(restful.Resource):

    @swagger.operation(
        nickname="getEndpoints",
        notes="Return full list of registered service urls, "
              "does't have any parameters.",
    )
    def get(self):
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Listing all endpoint urls.")

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
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Update endpoint.")

        status, value = manage_limits.endpoint_add(
            json['endpoint_url'], json['type'],
            json['version'], json['description'])

        return service_limit.general_response_todict(status, value)


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
        from walle_api_server.common import manage_limits

        restricted = service_limit.cant_edit_tenants()
        if restricted:
            return restricted

        logger.info("Delete  endpoint url.")

        _, value = manage_limits.endpoint_delete_id(id)

        return value
