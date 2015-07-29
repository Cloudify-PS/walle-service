# Copyright (c) 2015 VMware. All rights reserved

import json
import time

from score_api_server.tests.integration import base


class TestEvents(base.IntegrationBaseTestCase):

    def make_deployment_and_execution(self):
        response_bp = self.make_upload_blueprint()
        self.bp_content = json.loads(response_bp.data)
        deployment = self.make_deployment(self.bp_content['id'])
        deployment_content = json.loads(deployment.data)
        install_workflow = 'install'
        self.deployment_id = deployment_content['id'].replace(
            "{}_".format(self.org_id), "", 1)
        execution = self.make_execution(self.deployment_id, install_workflow)
        time.sleep(10)
        execution_content = json.loads(execution.data)
        self.execution_id = execution_content['id']

    def remove_deployments(self):
        content_type = 'application/json'
        data = {}
        self.execute_post_request_with_route(
            '/executions/%s' % self.execution_id, data=data,
            content_type=content_type)
        params = {'ignore_live_nodes': True}
        self.execute_delete_request_with_route(
            '/deployments/{0}'.format(self.deployment_id), params=params)
        self.execute_delete_request_with_route(
            '/blueprints/{0}'.format(self.bp_content['id']))

    def test_get_events(self):
        # make deployment and execution
        self.make_deployment_and_execution()

        content_type = 'application/json'
        data = {'execution_id': self.execution_id,
                'include_logs': 'true'}
        response = self.execute_post_request_with_route(
            "/events", data=json.dumps(data), content_type=content_type)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data)

        # remove deployments
        self.remove_deployments()
