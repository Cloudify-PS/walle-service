# Copyright (c) 2015 VMware. All rights reserved

import json
import git
import os
import tempfile
import testtools
import time
import uuid
import urllib
import shutil
import tarfile
import yaml
import shutil

from os.path import expanduser

from flask.ext.migrate import upgrade

from pyvcloud.vcloudsession import VCS

from walle_api_server.cli import app
from walle_api_server.db import models

from walle_api_server.tests import common
from walle_api_server.tests.fakes import exceptions
from walle_api_server.tests.fakes import vcloud_air_client
from walle_api_server.tests.fakes import cloudify_manager

RUN_INTEGRATION_TESTS = 'RunIntegrationTests'


class BaseWalleAPIClient(testtools.TestCase):

    def setUp(self):
        super(BaseWalleAPIClient, self).setUp()

    def tearDown(self):
        super(BaseWalleAPIClient, self).tearDown()

    def execute_get_request_with_route(self, route):
        pass

    def execute_delete_request_with_route(self, route):
        pass

    def execute_put_request_with_route(self, route,
                                       params=None,
                                       data=None):
        pass

    def execute_post_request_with_route(self, route,
                                        params=None,
                                        data=None):
        pass

    def try_auth(self, headers=None):
        pass

    def make_upload_blueprint(
            self,
            blueprint_filename="vcloud-blueprint-for-integration-tests.yaml",
            arc_type='tar'):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        blueprints_dir = current_dir + '/../../../../blueprints/'
        blueprint_path = blueprints_dir + blueprint_filename
        bp_id = str(uuid.uuid4()) + '_' + blueprint_filename
        response = self.upload_blueprint(blueprint_path, bp_id, arc_type)
        return response

    def upload_blueprint(self, blueprint_path, blueprint_id, arc_type):
        tempdir = tempfile.mkdtemp()
        try:
            if arc_type is 'tar':
                arc_path = self._tar_blueprint(blueprint_path, tempdir)
            else:
                arc_path = self._zip_blueprint(blueprint_path, tempdir)
            application_file = os.path.basename(blueprint_path)
            return self._upload(
                arc_path,
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

    def _zip_blueprint(self, blueprint_path, tempdir):

        blueprint_path = expanduser(blueprint_path)
        blueprint_name = os.path.basename(
            os.path.splitext(blueprint_path)[0])
        blueprint_directory = os.path.dirname(blueprint_path)
        if not blueprint_directory:
            # blueprint path only contains a file name from the local directory
            blueprint_directory = os.getcwd()
        arc_path = os.path.join(tempdir, blueprint_name)
        zip_path = shutil.make_archive(arc_path, 'zip',
                                       os.path.dirname(blueprint_directory),
                                       os.path.basename(blueprint_directory))
        return zip_path

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
                data=f.read())

    def make_deployment(self, blueprint_id):
        pass

    def make_execution(self, deployment_id, workflow_id):
        pass


class RealWalleAPIClient(BaseWalleAPIClient, common.vCloudLogin):

    def setUp(self):
        super(BaseWalleAPIClient, self).setUp()

        config_file = os.getenv('WALLE_INT_TESTS_CONF')
        if not config_file or not os.path.exists(config_file):
            raise exceptions.Unauthorized()
        with open(config_file, 'r') as stream:
            login_cfg = yaml.load(stream)

        cloudify_host = login_cfg.get('cloudify_host')
        cloudify_port = login_cfg.get('cloudify_port')
        deployment_limits = login_cfg.get('deployment_limits')
        self.service_version = login_cfg.get('service_version')

        # login to VCA
        attempt = 3
        while attempt:
            self.vca = self._login_to_vca(login_cfg)
            if self.vca:
                break
            attempt -= 1

        if not self.vca:
            raise exceptions.Unauthorized()

        # headers
        self.setup_headers()

        vcloud_org_url = self.vca.vcloud_session.org_url

        self.vcs = VCS(vcloud_org_url, None, None, None,
                       vcloud_org_url, vcloud_org_url,
                       version=self.service_version)

        # login to VCS
        result = self.vcs.login(token=self.headers['x-vcloud-authorization'])
        if not result:
            raise exceptions.Forbidden()
        self.org_id = self.vcs.organization.id[
            self.vcs.organization.id.rfind(':') + 1:]
        self.organization = models.AllowedOrgs(self.org_id)
        self.model_limits = models.OrgIDToCloudifyAssociationWithLimits(
            self.organization.org_id, cloudify_host, cloudify_port,
            deployment_limits=deployment_limits)

        self.addCleanup(self.vca.logout)

    def try_auth(self, headers=None):
        if not headers:
            self.vca.logout()
            return self.client.get('/', headers=headers)
        self.model_limits.delete()
        return self.client.get('/', headers=self.headers)

    def execute_get_request_with_route(self, route, params=None):
        return self.client.get(route, headers=self.headers,
                               query_string=params)

    def execute_delete_request_with_route(self, route, params=None):
        return self.client.delete(route, headers=self.headers,
                                  query_string=params)

    def execute_put_request_with_route(self, route, params=None, data=None,
                                       content_type=None):
        return self.client.put(route, headers=self.headers,
                               query_string=params, data=data,
                               content_type=content_type)

    def execute_post_request_with_route(self, route, params=None, data=None,
                                        content_type=None):
        return self.client.post(route, headers=self.headers,
                                query_string=params, data=data,
                                content_type=content_type)

    def make_deployment(self, blueprint_id):
        deployment_id = 'postgresql_test_deployment'
        response = self._start_deployment(blueprint_id, deployment_id)
        return response

    def _start_deployment(self, blueprint_id, deployment_id):
        content_type = 'application/json'
        data = {'blueprint_id': blueprint_id}
        return self.execute_put_request_with_route(
            '/deployments/%s' % deployment_id, data=json.dumps(data),
            content_type=content_type)

    def make_execution(self, deployment_id, workflow_id):
        params_deployment_id = {'deployment_id': deployment_id}
        attempt = 15
        print('Wait until execution will be available(attempts) \n'
              'attempts: %s' % attempt)
        while attempt:
            response = self.execute_get_request_with_route(
                "/executions", params=params_deployment_id)
            status = json.loads(response.data)[0]['status']
            if 'terminated' in status:
                return self._start_execution(deployment_id, workflow_id)
            time.sleep(10)
            attempt -= 1
            print('attempts: %s' % attempt)
        raise exceptions.Forbidden()

    def _start_execution(self, deployment_id, workflow_id,
                         allow_custom_parameters=False,
                         parameters=None, force=False):
        content_type = 'application/json'
        data = {
            'deployment_id': deployment_id,
            'workflow_id': workflow_id,
            'parameters': parameters,
            'allow_custom_parameters': allow_custom_parameters,
            'force': force
        }
        return self.execute_post_request_with_route(
            '/executions', data=json.dumps(data),
            content_type=content_type)


class FakeWalleAPIClient(BaseWalleAPIClient):

    reason_for_skipping = "This test-methods not supported.\n"

    def setUp(self):
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
        super(FakeWalleAPIClient, self).setUp()

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

    def execute_get_request_with_route(self, route, params=None):
        self.do_common_setup()
        return self.client.get(route, headers=self.headers,
                               query_string=params)

    def execute_delete_request_with_route(self, route, params=None):
        self.do_common_setup()
        return self.client.delete(route, headers=self.headers,
                                  query_string=params)

    def execute_put_request_with_route(self, route, params=None, data=None,
                                       content_type=None):
        self.do_common_setup()
        return self.client.put(route, headers=self.headers,
                               query_string=params, data=data,
                               content_type=content_type)

    def execute_post_request_with_route(self, route, params=None, data=None,
                                        content_type=None):
        self.do_common_setup()
        return self.client.post(route, headers=self.headers,
                                query_string=params, data=data,
                                content_type=content_type)

    @testtools.skip(reason_for_skipping)
    def make_deployment(self, blueprint_id):
        pass

    @testtools.skip(reason_for_skipping)
    def make_execution(self, deployment_id, workflow_id):
        pass

    def tearDown(self):
        app.VCS = self.safe_vcs
        app.CloudifyClient = self.safe_cfy
        vcloud_air_client.VCS.login = self.safe_login
        super(FakeWalleAPIClient, self).tearDown()


def _lookup_mode_value(message):
    found_string = filter(lambda x: RUN_INTEGRATION_TESTS in x,
                          message.split('\n'))[0]
    return found_string.split(' ')[1]


def _checking_commit_message(commit):
    for parent in commit.parents:
        if (RUN_INTEGRATION_TESTS in parent.message and
                _lookup_mode_value(parent.message) == 'True'):
            return True
    return False


def _checking_mode():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    git_dir = current_dir + '/../../../..'
    git_repo = git.repo.Repo(git_dir)
    commit = git_repo.commit()
    if (RUN_INTEGRATION_TESTS in commit.message and
            _lookup_mode_value(commit.message) == 'True'):
        return True
    return _checking_commit_message(commit)


def printing_message_which_base_class(base_class):
    message_which_base_class = 'Running tests with %s' % base_class.__name__
    print('-' * len(message_which_base_class))
    print(message_which_base_class)
    print('-' * len(message_which_base_class))


def get_base_class():
    test_mode = _checking_mode()
    base_class = (FakeWalleAPIClient
                  if test_mode is not True
                  else RealWalleAPIClient)
    printing_message_which_base_class(base_class)
    return base_class


class IntegrationBaseTestCase(get_base_class()):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()

        self.db_fd, self.db_fpath = tempfile.mkstemp()
        app.app.config['SQLALCHEMY_DATABASE_URI'] = (
            "sqlite:///%s.db" % self.db_fpath)

        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        with app.app.app_context():
            migrate_dir = self.current_dir + '/../../../migrations/'
            upgrade(directory=migrate_dir)
            models.base.db.create_all()

        approved_plugins = (self.current_dir +
                            '/../../../../approved_plugins/'
                            'approved_plugins_description.yaml')
        models.ApprovedPlugins.register_from_file(approved_plugins)

        super(IntegrationBaseTestCase, self).setUp()

    def recreate_approved_plugins(self):
        approved_plugins = (self.current_dir +
                            '/../../../../approved_plugins/'
                            'approved_plugins_description.yaml')
        models.ApprovedPlugins.register_from_file(approved_plugins)

    def drop_approved_plugins(self):
        for plugin in models.ApprovedPlugins.list():
            plugin.delete()

    def tearDown(self):

        for org_id in models.AllowedOrgs.list():
            org_id.delete()
        for org_id in models.OrgIDToCloudifyAssociationWithLimits.list():
            org_id.delete()

        os.close(self.db_fd)
        os.unlink(self.db_fpath)
        os.remove("%s.db" % self.db_fpath)

        super(IntegrationBaseTestCase, self).tearDown()
