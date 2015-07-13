# Copyright (c) 2015 VMware. All rights reserved

from flask.ext.restful import fields
from flask_restful_swagger import swagger


@swagger.model
class BlueprintState(object):

    resource_fields = {
        'id': fields.String,
        'plan': fields.Raw,
        'created_at': fields.String,
        'updated_at': fields.String
    }

    def __init__(self, **kwargs):
        self.plan = kwargs['plan']
        self.id = kwargs['id']
        self.created_at = kwargs['created_at']
        self.updated_at = kwargs['updated_at']


@swagger.model
class BlueprintValidationStatus(object):

    resource_fields = {
        'blueprintId': fields.String(attribute='blueprint_id'),
        'status': fields.String
    }

    def __init__(self, **kwargs):
        self.blueprint_id = kwargs['blueprint_id']
        self.status = kwargs['status']


@swagger.model
class Workflow(object):

    resource_fields = {
        'name': fields.String,
        'created_at': fields.String,
        'parameters': fields.Raw
    }

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.created_at = kwargs['created_at']
        self.parameters = kwargs['parameters']


@swagger.model
@swagger.nested(workflows=Workflow.__name__)
class Deployment(object):

    resource_fields = {
        'id': fields.String,
        'created_at': fields.String,
        'updated_at': fields.String,
        'blueprint_id': fields.String,
        'workflows': fields.List(fields.Nested(Workflow.resource_fields)),
        'inputs': fields.Raw,
        'policy_types': fields.Raw,
        'policy_triggers': fields.Raw,
        'groups': fields.Raw,
        'outputs': fields.Raw
    }

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.permalink = kwargs['permalink']
        self.created_at = kwargs['created_at']
        self.updated_at = kwargs['updated_at']
        self.blueprint_id = kwargs['blueprint_id']
        self.workflows = kwargs['workflows']
        self.inputs = kwargs['inputs']
        self.policy_types = kwargs['policy_types']
        self.policy_triggers = kwargs['policy_triggers']
        self.groups = kwargs['groups']
        self.outputs = kwargs['outputs']


@swagger.model
class DeploymentOutputs(object):

    resource_fields = {
        'deployment_id': fields.String,
        'outputs': fields.Raw
    }

    def __init__(self, **kwargs):
        self.deployment_id = kwargs['deployment_id']
        self.outputs = kwargs['outputs']


@swagger.model
class Execution(object):

    resource_fields = {
        'id': fields.String,
        'workflow_id': fields.String,
        'blueprint_id': fields.String,
        'deployment_id': fields.String,
        'status': fields.String,
        'error': fields.String,
        'created_at': fields.String,
        'parameters': fields.Raw,
        'is_system_workflow': fields.Boolean
    }

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.status = kwargs['status']
        self.deployment_id = kwargs['deployment_id']
        self.workflow_id = kwargs['workflow_id']
        self.blueprint_id = kwargs['blueprint_id']
        self.created_at = kwargs['created_at']
        self.error = kwargs['error']
        self.parameters = kwargs['parameters']
        self.is_system_workflow = kwargs['is_system_workflow']


@swagger.model
class Status(object):

    resource_fields = {
        'status': fields.String,
        'services': fields.Raw
    }

    def __init__(self, **kwargs):
        self.status = kwargs['status']
        self.services = kwargs['services']


@swagger.model
class Login(object):

    resource_fields = {
        'x_vcloud_authorization': fields.String,
        'x_vcloud_org_url': fields.String,
        'x_vcloud_version': fields.String
    }

    def __init__(self, **kwargs):
        self.x_vcloud_authorization = kwargs['x_vcloud_authorization']
        self.x_vcloud_org_url = kwargs['x_vcloud_org_url']
        self.x_vcloud_version = kwargs['x_vcloud_version']
