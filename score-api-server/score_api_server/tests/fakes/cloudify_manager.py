# Copyright (c) 2015 VMware. All rights reserved

from cloudify_rest_client import exceptions

BP_DB = {}


class BlueprintsManager(object):

    def __init__(self):
        pass

    def get(self, blueprint_id):
        # bp = BP_DB.get(blueprint_id)
        # if not bp:
        raise exceptions.CloudifyClientError(
            "Blueprint with ID:%s not found." % blueprint_id,
            status_code=404)
        # return bp

    def list(self):
        return BP_DB.values()

    def delete(self, bp_id):
        self.get(bp_id)
        del BP_DB[bp_id]


class CloudifyClient(object):
    """Cloudify's management client."""

    def __init__(self, host='localhost', port=None, protocol=None,
                 headers=None, query_params=None, cert=None, trust_all=False):
        """Creates a Cloudify client with the provided host and optional port.

        :param host: Host of Cloudify's management machine.
        :param port: Port of REST API service on management machine.
        :param protocol: Protocol of REST API service on management machine,
                        defaults to http.
        :param headers: Headers to be added to request.
        :param query_params: Query parameters to be added to the request.
        :param cert: Path to a copy of the server's self-signed certificate.
        :param trust_all: if `False`, the server's certificate
                          (self-signed or not) will be verified.
        :return: Cloudify client instance.
        """

        self.blueprints = BlueprintsManager()
