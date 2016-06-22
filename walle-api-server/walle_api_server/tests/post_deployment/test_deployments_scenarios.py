# Copyright (c) 2015 VMware. All rights reserved

import uuid

from walle_api_server.tests.post_deployment import base


class TestDeploymentScenarios(base.BasePostDeploymentTestCase):

    def test_deployment_scenarios(self):
        """Test scenarios #1

                1. Upload blueprint
                2. Create deployment
                3. List deployments
                4. Get deployment.
                5. Delete deployment.
                5. Delete blueprint.
        """
        try:

            blueprint_id = str(uuid.uuid4())
            deployment_id = "deployment_for_{0}".format(blueprint_id)

            uploaded_blueprint = self.walle_client.blueprints.upload(
                self.valid_blueprint_path, blueprint_id)
            self.printer("1. Upload blueprint. Passed.",
                         self.walle_client.response.json())

            self.assertIsNotNone(uploaded_blueprint)
            self.assertEqual(
                200, self.walle_client.response.status_code)
            self.assertEqual(uploaded_blueprint['id'], blueprint_id)

            deployment = self.walle_client.deployments.create(
                blueprint_id, deployment_id, inputs='{}')
            self.printer("2. Create deployment. Passed.",
                         self.walle_client.response.json())

            self.assertIsNotNone(deployment)
            self.assertEqual(deployment['blueprint_id'], blueprint_id)
            self.assertEqual(deployment['id'], deployment_id)

            deployments = self.walle_client.deployments.list()
            self.printer("3. List deployments. Passed.",
                         self.walle_client.response.json())

            self.assertIsNotNone(deployments)
            self.assertNotEqual(0, len(deployments))

            get_deployment = self.walle_client.deployments.get(deployment_id)
            self.printer("4. Get deployment. Passed.",
                         self.walle_client.response.json())

            self.assertIsNotNone(get_deployment)
            self.assertEqual(deployment_id,
                             get_deployment['id'])

            def wait_until_execution_is_finished():
                executions = self.walle_client.executions.list(deployment_id)
                statuses = [execution['status'] for execution in executions]
                if len(set(statuses)) == 1 and statuses[0] == 'terminated':
                    return True
                else:
                    return False

            base.poll_until(wait_until_execution_is_finished,
                            expected_result=True)

            self.walle_client.deployments.delete(deployment_id)
            self.printer("5. Delete deployment. Passed.",
                         self.walle_client.response.json())
            self.walle_client.blueprints.delete(blueprint_id)
            self.printer("6. Delete blueprint. Passed.",
                         self.walle_client.response.json())

        except Exception as e:
            self.printer(str(e))
            print(self.walle_client.response.content)
            print(self.walle_client.response.status_code)
            raise e
