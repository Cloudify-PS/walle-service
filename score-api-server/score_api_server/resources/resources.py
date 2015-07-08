# Copyright (c) 2015 VMware. All rights reserved

from score_api_server.resources import swagger as rest_swagger
from score_api_server.resources import blueprints
from score_api_server.resources import deployments
from score_api_server.resources import executions
from score_api_server.resources import events
from score_api_server.resources import status

SUPPORTED_API_VERSIONS = ['v1']


def _versioned_urls(endpoint):
    urls = []
    for api_version in SUPPORTED_API_VERSIONS:
        urls.append('/{0}/{1}'.format(api_version, endpoint))
    return urls


def setup_resources(api):
    resources_endpoints = {
        blueprints.Blueprints: 'blueprints',
        blueprints.BlueprintsId: 'blueprints/<string:blueprint_id>',
        deployments.Deployments: 'deployments',
        deployments.DeploymentsId: 'deployments/<string:deployment_id>',
        executions.Executions: 'executions',
        events.Events: 'events',
        status.Status: 'status',
    }

    for resource, endpoint in resources_endpoints.iteritems():
        api.add_resource(resource, *_versioned_urls(endpoint))

        for api_version in SUPPORTED_API_VERSIONS:
            rest_swagger.add_swagger_resource(
                api, api_version, resource, '/{0}/{1}'.format(api_version,
                                                              endpoint))
