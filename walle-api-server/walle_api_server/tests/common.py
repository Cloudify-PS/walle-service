# Copyright (c) 2015 VMware. All rights reserved

import os
import yaml

from pyvcloud.vcloudair import VCA

from walle_api_server.tests.fakes import exceptions


class vCloudLogin(object):

    def setup_headers(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        path_to_login_json = (current_dir +
                              '/../../real-mode-tests-conf.yaml')
        with open(path_to_login_json, 'r') as stream:
            login_cfg = yaml.load(stream)
        self.service_version = login_cfg.get('service_version')
        self.walle_url = login_cfg.get(
            "walle_url",
            os.getenv("WALLE_URL",
                      "http://localhost:8000"))

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
        self.headers = {
            'x-vcloud-authorization': self.vca.vcloud_session.token,
            'x-vcloud-org-url': self.vca.vcloud_session.org_url,
            'x-vcloud-version': self.service_version,
        }

    def _login_to_vca(self, login_json):
        request_json = login_json
        if request_json:
            user = request_json.get('user')
            password = request_json.get('password')
            service_type = request_json.get('service_type', 'subscription')
            host = request_json.get('host', 'https://vchs.vmware.com')
            org_name = request_json.get('org_name')
            service = request_json.get('service')
            vca = self._login_user_to_service(user, host,
                                              password, service_type,
                                              self.service_version,
                                              service, org_name)
            return vca

    def _login_user_to_service(self, user, host, password, service_type,
                               service_version, service, org_name):
        vca = VCA(host, user, service_type, service_version)
        result = vca.login(password=password)
        if result:
            if service_type == 'subscription':
                if not service:
                    if org_name:
                        service = org_name
                    else:
                        services = vca.services.get_Service()
                        if not services:
                            return None
                        service = services[0].serviceId
                if not org_name:
                    org_name = vca.get_vdc_references(service)[0].name
                result = vca.login_to_org(service, org_name)
            if result:
                return vca
        return
