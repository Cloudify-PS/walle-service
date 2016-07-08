# Copyright (c) 2015 VMware. All rights reserved

import flask
import uuid

from walle_api_server.common import service_limit
from walle_api_server.cli import app
from walle_api_server.db.models import Endpoint
from walle_api_server.db.models import Limit
from walle_api_server.db.models import Tenant

from walle_api_server.tests.unittests import base


class EndpointTenantLimitTest(base.BaseTestCaseWihtBackend):

    def setUp(self):
        super(EndpointTenantLimitTest, self).setUp()
        self.prefix = str(uuid.uuid4())
        self._create_tenant_orgs()

    def tearDown(self):
        super(EndpointTenantLimitTest, self).tearDown()

    def _create_tenant_orgs(self):
        # add some values
        org = Endpoint(self.prefix + "some_id", "openstack")
        k_org = Endpoint(self.prefix + "k_id", "openstack")
        self.obj_list.append(k_org)
        self.obj_list.append(org)

    def test_get_current_limit(self):
        """get current limit for organizations"""

        with app.app.app_context():
            # check value for current existed
            flask.g.endpoint_url = self.prefix + "some_id"
            endpoint = service_limit.check_endpoint_url(
                flask.g.endpoint_url, "openstack"
            )
            self.assertTrue(endpoint)
            self.assertIn(self.prefix + "some_id",
                          endpoint.endpoint)
            # check count
            flask.g.endpoint_url = self.prefix + "k_id"
            endpoint = service_limit.check_endpoint_url(
                flask.g.endpoint_url, "openstack"
            )
            self.assertTrue(endpoint)
            self.assertIn(self.prefix + "k_id", endpoint.endpoint)
            # no orgs
            flask.g.endpoint_url = self.prefix + "some_other_id"
            endpoint = service_limit.check_endpoint_url(
                flask.g.endpoint_url, "openstack"
            )
            self.assertFalse(endpoint)


class TestDeploymentLimitsDBModel(base.BaseTestCaseWihtBackend):

    def setUp(self):
        super(TestDeploymentLimitsDBModel, self).setUp()
        self.allowed_endpoint = Endpoint(
            str(uuid.uuid4()), type='openstack', version='*',
            description="test_org_id"
        )
        self.obj_list.append(self.allowed_endpoint)

    def tearDown(self):
        super(TestDeploymentLimitsDBModel, self).tearDown()

    def create_tenant(self):
        return Tenant(
            self.allowed_endpoint.id,
            "some_tenant",
            "127.0.0.1",
            "80"
        )

    def test_create_successfuly(self):
        successful_tenant = self.create_tenant()

        self.assertIsNotNone(successful_tenant)
        self.assertIsNotNone(successful_tenant.endpoint_id)
        self.assertEqual(self.allowed_endpoint.id,
                         successful_tenant.endpoint_id)
        self.assertIsNotNone(successful_tenant.id)
        self.assertIsNotNone(successful_tenant.created_at)
        self.assertIsNotNone(successful_tenant.updated_at)
        self.assertEqual("127.0.0.1",
                         successful_tenant.cloudify_host)
        self.assertEqual(80, successful_tenant.cloudify_port)

        successful_tenant.delete()

    def test_create_duplicate_org_id_host_port(self):
        limit = self.create_tenant()

        self.assertRaises(Exception,
                          Tenant.__init__,
                          self.allowed_endpoint.id,
                          "127.0.0.1",
                          "80")
        self.assertRaises(Exception,
                          Tenant.__init__,
                          self.allowed_endpoint.id,
                          "127.0.0.2",
                          "8889")

        limit.delete()

    def test_list_limits(self):
        limit = self.create_tenant()

        limits = Tenant.list()
        self.assertNotEqual(0, len(limits))

        limit.delete()

    def test_find_by(self):
        limit = self.create_tenant()

        limit_by_id = Tenant.find_by(
            id=limit.id)
        limit_by_org_id = Tenant.find_by(
            endpoint_id=limit.endpoint_id)
        self.assertEqual(limit_by_id.created_at, limit_by_org_id.created_at)

        limit.delete()

    def test_update(self):
        limit = self.create_tenant()

        patched_limit = limit.update(cloudify_host="127.0.0.100",
                                     deployment_limits=100,
                                     number_of_deployments=99)
        self.assertEqual(limit.endpoint_id, patched_limit.endpoint_id)
        self.assertEqual(limit.id, patched_limit.id)

        patched_limit.delete()

    def test_get_current_credentials_and_limits(self):
        tenant = self.create_tenant()

        with app.app.app_context():
            flask.g.endpoint_url = self.allowed_endpoint.endpoint
            _tenant = service_limit.get_endpoint_tenant(
                flask.g.endpoint_url, "openstack", "some_tenant"
            )
            self.assertEqual(tenant.cloudify_host,
                             _tenant.cloudify_host)
            self.assertEqual(tenant.cloudify_port,
                             _tenant.cloudify_port)
            self.assertEqual(tenant.endpoint_id, _tenant.endpoint_id)

            limit = Limit(
                tenant.id, soft=100, hard=50, type="ram", value=-5
            )

            _limit = service_limit.get_endpoint_tenant_limit(
                flask.g.endpoint_url, "openstack", "some_tenant", "none"
            )
            self.assertFalse(_limit)
            _limit = service_limit.get_endpoint_tenant_limit(
                flask.g.endpoint_url, "openstack", "some_tenant", "ram"
            )
            self.assertEqual(limit.hard, _limit.hard)
            self.assertEqual(limit.soft, _limit.soft)
            self.assertEqual(limit.value, _limit.value)
