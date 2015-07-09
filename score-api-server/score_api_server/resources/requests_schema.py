# Copyright (c) 2015 VMware. All rights reserved

from flask.ext.restful import fields
from flask_restful_swagger import swagger


@swagger.model
class ExecutionRequest(object):

    resource_fields = {
        'workflow_id': fields.String,
        'parameters': fields.Raw,
        'allow_custom_parameters': fields.Boolean,
        'force': fields.Boolean
    }


@swagger.model
class ModifyExecutionRequest(object):

    resource_fields = {
        'action': fields.String
    }
