# Copyright (c) 2015 VMware. All rights reserved

import os
import tempfile
import testtools
import urllib
import shutil
import tarfile

from os.path import expanduser

from flask.ext.migrate import upgrade

from score_api_server.cli import app
from score_api_server.db import models

from score_api_server.tests.fakes import vcloud_air_client
from score_api_server.tests.fakes import cloudify_manager


class BaseScoreAPIClient(testtools.TestCase):

    def setUp(self):
        super(BaseScoreAPIClient, self).setUp()

    def tearDown(self):
        super(BaseScoreAPIClient, self).tearDown()

    def execute_get_request_with_route(self, route):
        pass

    def execute_delete_request_with_route(self, route):
        pass

    def execute_put_request_with_route(self, route,
                                       params=None,
                                       data=None):
        pass

    def try_auth(self, headers=None):
        pass

    def make_upload(self):
        pass


class RealScoreAPIClient(BaseScoreAPIClient):

    reason_for_skipping = ("Real-mode integration "
                           "testing not supported.\n")

    def setUp(self):
        super(BaseScoreAPIClient, self).setUp()

    def tearDown(self):
        super(BaseScoreAPIClient, self).tearDown()

    @testtools.skip(reason_for_skipping)
    def execute_get_request_with_route(self, route):
        pass

    @testtools.skip(reason_for_skipping)
    def execute_delete_request_with_route(self, route):
        pass

    @testtools.skip(reason_for_skipping)
    def execute_put_request_with_route(self, route,
                                       params=None,
                                       data=None):
        pass

    @testtools.skip(reason_for_skipping)
    def try_auth(self, headers=None):
        pass

    @testtools.skip(reason_for_skipping)
    def make_upload_blueprint(self):
        pass


class FakeScoreAPIClient(BaseScoreAPIClient):

    def setUp(self):
        app.app.config['TESTING'] = True
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
        super(FakeScoreAPIClient, self).setUp()

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

    def try_auth(self, headers=None):
        return self.client.get('/', headers=headers)

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

    def make_upload_blueprint(self):
        # TODO(???) make blueprint path configurable
        blueprint_filename = "vcloud-postgresql-blueprint.yaml"
        current_dir = os.path.dirname(os.path.realpath(__file__))
        blueprints_dir = current_dir + '/../../../../blueprints/'
        blueprint_path = blueprints_dir + blueprint_filename
        response = self.upload_blueprint(blueprint_path,
                                         blueprint_filename)
        return response

    def upload_blueprint(self, blueprint_path, blueprint_id):
        tempdir = tempfile.mkdtemp()
        try:
            tar_path = self._tar_blueprint(blueprint_path, tempdir)
            application_file = os.path.basename(blueprint_path)
            return self._upload(
                tar_path,
                blueprint_id=blueprint_id,
                application_file_name=application_file)
        finally:
            shutil.rmtree(tempdir)

    def _tar_blueprint(self, blueprint_path, tempdir):

        blueprint_path = expanduser(blueprint_path)
        blueprint_name = os.path.basename(
            os.path.splitext(blueprint_path)[0])
        blueprint_directory = os.path.dirname(blueprint_path)

        if not blueprint_directory:
            # blueprint path only contains a file name from the local directory
            blueprint_directory = os.getcwd()
        tar_path = os.path.join(
            tempdir, '{0}.tar.gz'.format(blueprint_name))

        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(
                blueprint_directory,
                arcname=os.path.basename(blueprint_directory))

        return tar_path

    def _upload(self, tar_file,
                blueprint_id,
                application_file_name=None):
        query_params = {}
        if application_file_name is not None:
            query_params[
                'application_file_name'] = urllib.quote(
                application_file_name)

        with open(tar_file, 'rb') as f:
            return self.execute_put_request_with_route(
                '/blueprints/{0}'.format(blueprint_id),
                params=query_params,
                data=f.read()
            )

    def tearDown(self):
        app.VCS = self.safe_vcs
        app.CloudifyClient = self.safe_cfy
        vcloud_air_client.VCS.login = self.safe_login
        super(FakeScoreAPIClient, self).tearDown()


def get_base_class():
    score_api_client_type = os.environ.get(
        "SCORE_INTEGRATION_TEST_TYPE", "fake")
    base_class = (FakeScoreAPIClient
                  if score_api_client_type == "fake"
                  else RealScoreAPIClient)
    return base_class


class IntegrationBaseTestCase(get_base_class()):

    def setUp(self):
        self.db_fd, self.db_fpath = tempfile.mkstemp()
        app.app.config['SQLALCHEMY_DATABASE_URI'] = (
            "sqlite:///%s.db" % self.db_fpath)

        current_dir = os.path.dirname(os.path.realpath(__file__))
        with app.app.app_context():
            migrate_dir = current_dir + '/../../../migrations/'
            upgrade(directory=migrate_dir)
            app.db.create_all()

        super(IntegrationBaseTestCase, self).setUp()

    def tearDown(self):

        for org_id in models.AllowedOrgs.list():
            org_id.delete()
        for org_id in models.OrgIDToCloudifyAssociationWithLimits.list():
            org_id.delete()

        os.close(self.db_fd)
        os.unlink(self.db_fpath)
        os.remove("%s.db" % self.db_fpath)

        super(IntegrationBaseTestCase, self).tearDown()
