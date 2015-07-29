# Copyright (c) 2015 VMware. All rights reserved

import uuid

from cloudify_rest_client import exceptions

BP_DB = {}


class Blueprint(dict):

    def __init__(self, obj_id, obj_blueprint_id, obj_deployment_id):
        self.setdefault('id', obj_id)
        self.blueprint_id = obj_blueprint_id
        self.deployment_id = obj_deployment_id
        super(Blueprint, self).__init__(self.to_dict())

    @property
    def id(self):
        return self.get('id')

    def to_dict(self):
        return {
            "id": self.blueprint_id,
            "deployment_id": self.deployment_id
        }


class BlueprintsManager(object):

    def get(self, blueprint_id):
        _bp = None
        try:
            _, _, bp_obj_id = blueprint_id.split("_")
        except Exception:
            bp_obj_id = blueprint_id
        for key, bp_values in BP_DB.items():
            if bp_obj_id == bp_values.blueprint_id.split("_")[2]:
                _bp = bp_values
                return _bp
        if not _bp:
            raise exceptions.CloudifyClientError(
                "Blueprint with ID:%s not found." % blueprint_id,
                status_code=404)

    def list(self):
        return BP_DB.values()

    def delete(self, bp_id):
        try:
            org_id, bp_obj_id = bp_id.split("_")
        except Exception:
            bp_obj_id = bp_id

        self.get(bp_id)
        for key, bp_values in BP_DB.items():
            if bp_obj_id == bp_values.id:
                del BP_DB[key]
                return

    def upload(self, blueprint_path, blueprint_id):
        # TODO(???): Once BP download feature appeares,
        # TODO(???): it would require to create an archive from BP
        # TODO(???):path and store it
        bp = Blueprint(str(uuid.uuid4()),
                       blueprint_id,
                       str(uuid.uuid4()))
        BP_DB[blueprint_id] = bp
        return bp.to_dict()


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
