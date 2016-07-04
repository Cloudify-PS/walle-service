# Copyright (c) 2015 VMware. All rights reserved

import flask
import uuid

from walle_api_server.common import service_limit
from walle_api_server.cli import app
from walle_api_server.db.models import AllowedServiceUrl
from walle_api_server.db.models import (
    ServiceUrlToCloudifyAssociationWithLimits)

from walle_api_server.tests.unittests import base


class CommonOrgLimitTest(base.BaseTestCaseWihtBackend):

    def setUp(self):
        super(CommonOrgLimitTest, self).setUp()
        self.prefix = str(uuid.uuid4())
        self._create_limit_orgs()

    def tearDown(self):
        super(CommonOrgLimitTest, self).tearDown()

    def _create_limit_orgs(self):
        # add some values
        org = AllowedServiceUrl('some_url', self.prefix + "some_id")
        k_org = AllowedServiceUrl('some_url', self.prefix + "k_id")
        self.obj_list.append(k_org)
        self.obj_list.append(org)

    def test_get_current_limit(self):
        """get current limit for organizations"""

        with app.app.app_context():
            # check value for current existed
            flask.g.tenant_id = self.prefix + "some_id"
            limit = service_limit.check_service_url('some_url',
                                                    flask.g.tenant_id)
            self.assertTrue(limit)
            self.assertIn(self.prefix + "some_id",
                          limit.tenant)
            # check count
            flask.g.tenant_id = self.prefix + "k_id"
            limit = service_limit.check_service_url('some_url',
                                                    flask.g.tenant_id)
            self.assertTrue(limit)
            self.assertIn(self.prefix + "k_id", limit.tenant)
            # no orgs
            flask.g.tenant_id = self.prefix + "some_other_id"
            limit = service_limit.check_service_url('some_url',
                                                    flask.g.tenant_id)
            self.assertFalse(limit)


class TestDeploymentLimitsDBModel(base.BaseTestCaseWihtBackend):

    def setUp(self):
        super(TestDeploymentLimitsDBModel, self).setUp()
        self.allowed_service_url = AllowedServiceUrl(
            'some_url',
            str(uuid.uuid4()),
            info="test_org_id"
        )
        self.obj_list.append(self.allowed_service_url)

    def tearDown(self):
        super(TestDeploymentLimitsDBModel, self).tearDown()

    def create_limit(self):
        return ServiceUrlToCloudifyAssociationWithLimits(
            self.allowed_service_url.id,
            "127.0.0.1",
            "80",
        )

    def test_create_successfuly(self):
        successful_limit = self.create_limit()

        self.assertIsNotNone(successful_limit)
        self.assertIsNotNone(successful_limit.serviceurl_id)
        self.assertEqual(self.allowed_service_url.id,
                         successful_limit.serviceurl_id)
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
                          ServiceUrlToCloudifyAssociationWithLimits.__init__,
                          self.allowed_service_url.id,
                          "127.0.0.1",
                          "80")
        self.assertRaises(Exception,
                          ServiceUrlToCloudifyAssociationWithLimits.__init__,
                          self.allowed_service_url.id,
                          "127.0.0.2",
                          "8889")

        limit.delete()

    def test_list_limits(self):
        limit = self.create_limit()

        limits = ServiceUrlToCloudifyAssociationWithLimits.list()
        self.assertNotEqual(0, len(limits))

        limit.delete()

    def test_find_by(self):
        limit = self.create_limit()

        limit_by_id = ServiceUrlToCloudifyAssociationWithLimits.find_by(
            id=limit.id)
        limit_by_org_id = ServiceUrlToCloudifyAssociationWithLimits.find_by(
            serviceurl_id=limit.serviceurl_id)
        self.assertEqual(limit_by_id.created_at, limit_by_org_id.created_at)

        limit.delete()

    def test_update(self):
        limit = self.create_limit()

        patched_limit = limit.update(cloudify_host="127.0.0.100",
                                     deployment_limits=100,
                                     number_of_deployments=99)
        self.assertEqual(limit.serviceurl_id, patched_limit.serviceurl_id)
        self.assertEqual(limit.id, patched_limit.id)

        patched_limit.delete()

    def test_get_current_credentials_and_limits(self):
        limit = self.create_limit()

        with app.app.app_context():
            flask.g.tenant_id = self.allowed_service_url.tenant
            _limit = (
                service_limit.get_service_url_limits('some_url',
                                                     flask.g.tenant_id))
            self.assertEqual(limit.cloudify_host,
                             _limit.cloudify_host)
            self.assertEqual(limit.cloudify_port,
                             _limit.cloudify_port)
            self.assertEqual(limit.serviceurl_id, _limit.serviceurl_id)
