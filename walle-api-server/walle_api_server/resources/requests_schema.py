# Copyright (c) 2015 VMware. All rights reserved

from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class ExecutionRequest(object):

    resource_fields = {
        'deployment_id': fields.String,
        'workflow_id': fields.String,
        'parameters': fields.Raw,
        'allow_custom_parameters': fields.Boolean,
        'force': fields.Boolean
    }


@swagger.model
class ModifyExecutionRequest(object):

    resource_fields = {
        'force': fields.Boolean
    }
