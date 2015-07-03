# Copyright (c) 2015 VMware. All rights reserved

import flask
import uuid

from score_api_server.common import org_limit
from score_api_server.cli import app
from score_api_server.db.models import AllowedOrgs
from score_api_server.db.models import (
    OrgIDToCloudifyAssociationWithLimits)

from score_api_server.tests.unittests import base


class CommonOrgLimitTest(base.BaseTestCaseWihtBackend):

    def setUp(self):
        super(CommonOrgLimitTest, self).setUp()
        self.prefix = str(uuid.uuid4())
        self._create_limit_orgs()

    def tearDown(self):
        super(CommonOrgLimitTest, self).tearDown()

    def _create_limit_orgs(self):
        # add some values
        org = AllowedOrgs(self.prefix + "some_id")
        k_org = AllowedOrgs(self.prefix + "k_id")
        self.obj_list.append(k_org)
        self.obj_list.append(org)

    def test_get_current_limit(self):
        """get current limit for organizations"""

        with app.app.app_context():
            # check value for current existed
            flask.g.org_id = self.prefix + "some_id"
            limit = org_limit.check_org_id()
            self.assertTrue(limit)
            self.assertIn(self.prefix + "some_id",
                          limit.org_id)
            # check count
            flask.g.org_id = self.prefix + "k_id"
            limit = org_limit.check_org_id()
            self.assertTrue(limit)
            self.assertIn(self.prefix + "k_id", limit.org_id)
            # no orgs
            flask.g.org_id = self.prefix + "some_other_id"
            limit = org_limit.check_org_id()
            self.assertFalse(limit)


class TestDeploymentLimitsDBModel(base.BaseTestCaseWihtBackend):

    def setUp(self):
        super(TestDeploymentLimitsDBModel, self).setUp()
        self.allowed_org_id = AllowedOrgs(
            str(uuid.uuid4()),
            info="test_org_id"
        )
        self.obj_list.append(self.allowed_org_id)

    def tearDown(self):
        super(TestDeploymentLimitsDBModel, self).tearDown()

    def create_limit(self):
        return OrgIDToCloudifyAssociationWithLimits(
            self.allowed_org_id.org_id,
            "127.0.0.1",
            "80",
        )

    def test_create_successfuly(self):
        successful_limit = self.create_limit()

        self.assertIsNotNone(successful_limit)
        self.assertIsNotNone(successful_limit.org_id)
        self.assertEqual(self.allowed_org_id.org_id,
                         successful_limit.org_id)
        self.assertIsNotNone(successful_limit.id)
        self.assertIsNotNone(successful_limit.created_at)
        self.assertIsNotNone(successful_limit.updated_at)
        self.assertEqual("127.0.0.1",
                         successful_limit.cloudify_host)
        self.assertEqual("80", successful_limit.cloudify_port)

        successful_limit.delete()

    def test_create_duplicate_org_id_host_port(self):
        limit = self.create_limit()

        self.assertRaises(Exception,
                          OrgIDToCloudifyAssociationWithLimits.__init__,
                          self.allowed_org_id.org_id,
                          "127.0.0.1",
                          "80")
        self.assertRaises(Exception,
                          OrgIDToCloudifyAssociationWithLimits.__init__,
                          self.allowed_org_id.org_id,
                          "127.0.0.2",
                          "8889")

        limit.delete()

    def test_list_limits(self):
        limit = self.create_limit()

        limits = OrgIDToCloudifyAssociationWithLimits.list()
        self.assertNotEqual(0, len(limits))

        limit.delete()

    def test_find_by(self):
        limit = self.create_limit()

        limit_by_id = OrgIDToCloudifyAssociationWithLimits.find_by(
            id=limit.id)
        limit_by_org_id = OrgIDToCloudifyAssociationWithLimits.find_by(
            org_id=limit.org_id)
        self.assertEqual(limit_by_id.created_at, limit_by_org_id.created_at)

        limit.delete()

    def test_update(self):
        limit = self.create_limit()

        patched_limit = limit.update(cloudify_host="127.0.0.100",
                                     deployment_limits=100,
                                     number_of_deployments=99)
        self.assertEqual(limit.org_id, patched_limit.org_id)
        self.assertEqual(limit.id, patched_limit.id)

        patched_limit.delete()

    def test_get_current_credentials_and_limits(self):
        limit = self.create_limit()

        with app.app.app_context():
            flask.g.org_id = self.allowed_org_id.org_id
            _limit, cfy_host, cfy_port = (
                org_limit.get_cloudify_credentials_and_org_id_limit())
            self.assertEqual(limit.cloudify_host, cfy_host)
            self.assertEqual(limit.cloudify_port, cfy_port)
            self.assertEqual(limit.org_id, _limit.org_id)
