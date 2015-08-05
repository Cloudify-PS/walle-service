# Copyright (c) 2015 VMware. All rights reserved

import os
import testtools

from pyvcloud import score

from score_api_server.tests import common


class BasePostDeploymentTestCase(testtools.TestCase, common.vCloudLogin):

    def setUp(self):
        self.setup_headers()

        self.printer("Using Score at {0}".format(self.score_url))

        self.score_client = score.Score(
            self.score_url,
            token=self.headers['x-vcloud-authorization'],
            org_url=self.headers['x-vcloud-org-url'],
            version=self.headers['x-vcloud-version']
        )
        current_dir = os.path.dirname(os.path.realpath(__file__))
        blueprints_dir = current_dir + '/../../../../blueprints/'
        self._valid_blueprint_path = (
            blueprints_dir + "vcloud-blueprint-for-tests.yaml")

        self.valid_blueprint_path = os.getenv("SCORE_VALID_BLUEPRINT",
                                              self._valid_blueprint_path)

        self.addCleanup(self.vca.logout)

        super(BasePostDeploymentTestCase, self).setUp()

    def printer(self, message, response=""):
        print("-" * len(message))
        print(message)
        print(str(response))
        print("-" * len(message))


def poll_until(pollster, expected_result=None, sleep_time=5):
    import time
    if not callable(pollster):
        raise Exception("%s is not callable" % pollster.__name__)
    while pollster() != expected_result:
        time.sleep(sleep_time)
