# Copyright (c) 2015 VMware. All rights reserved

import os
import tempfile
import testtools

from flask.ext.migrate import upgrade

from score_api_server.cli import app
from score_api_server.db import models

from score_api_server.tests.fakes import vcloud_air_client
from score_api_server.tests.fakes import cloudify_manager


class IntegrationBaseTestCase(testtools.TestCase):

    def setUp(self):
        self.db_fd, self.db_fpath = tempfile.mkstemp()
        app.app.config['SQLALCHEMY_DATABASE_URI'] = (
            "sqlite:///%s.db" % self.db_fpath)
        app.app.config['TESTING'] = True

        current_dir = os.path.dirname(os.path.realpath(__file__))
        with app.app.app_context():
            migrate_dir = current_dir + '/../../../migrations/'
            upgrade(directory=migrate_dir)
            app.db.create_all()

        self.client = app.app.test_client()

        # monkey-patching VCS class to
        # disable vCloud Air logging
        self.safe_vcs = app.VCS
        app.VCS = vcloud_air_client.VCS

        # monkey-patching Cloudify ReST client with
        # fake implementation of it
        self.safe_cfy = app.CloudifyClient
        app.CloudifyClient = cloudify_manager.CloudifyClient

        self.safe_login = vcloud_air_client.VCS.login
        self.headers = {
            "x-vcloud-authorization": "True",
            "x-vcloud-org-url": "URL",
            "x-vcloud-version": "some_version"
        }
        super(IntegrationBaseTestCase, self).setUp()

    def do_common_setup(self):

        def login(self, **kwargs):
            self.organization = self.Org()
            models.OrgIDToCloudifyAssociationWithLimits(
                self.organization.id,
                "127.0.0.1",
                "80",
                deployment_limits=-1,
            )
            return self

        vcloud_air_client.VCS.login = login

    def execute_get_request_with_route(self, route):
        self.do_common_setup()
        return self.client.get(route, headers=self.headers)

    def execute_delete_request_with_route(self, route):
        self.do_common_setup()
        return self.client.delete(route, headers=self.headers)

    def execute_put_request_with_route(self, route,
                                       params=None, data=None):
        self.do_common_setup()
        return self.client.put(route,
                               headers=self.headers,
                               query_string=params,
                               data=data)

    def tearDown(self):

        for org_id in models.AllowedOrgs.list():
            org_id.delete()

        for org_id in models.OrgIDToCloudifyAssociationWithLimits.list():
            org_id.delete()

        os.close(self.db_fd)
        os.unlink(self.db_fpath)
        os.remove("%s.db" % self.db_fpath)

        app.VCS = self.safe_vcs
        app.CloudifyClient = self.safe_cfy
        vcloud_air_client.VCS.login = self.safe_login

        super(IntegrationBaseTestCase, self).tearDown()
