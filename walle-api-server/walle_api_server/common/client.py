import requests
import json
from requests.packages import urllib3
from walle_api_server.common import util

DEFAULT_PORT = 80
SECURED_PORT = 443
SECURED_PROTOCOL = 'https'
DEFAULT_PROTOCOL = 'http'
DEFAULT_API_VERSION = 'v2.1'


urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)


class HTTPException(Exception):

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


def _check_exception(response):
    if response.status_code != requests.codes.ok:
        raise HTTPException(response.content)


class HTTPClient(object):

    def __init__(self, host, port=DEFAULT_PORT,
                 protocol=DEFAULT_PROTOCOL, api_version=DEFAULT_API_VERSION,
                 headers=None, query_params=None, cert=None, trust_all=False):
        self.port = port
        self.host = host
        self.url = '{0}://{1}:{2}/api/{3}'.format(protocol, host, port,
                                                  api_version)
        self.headers = headers.copy() if headers else {}
        if not self.headers.get('Content-type'):
            self.headers['Content-type'] = 'application/json'

    def get(self, request):
        path = request.path
        parameters = dict(request.args)
        if request.args.get('id'):
            id = request.args['id']
            parameters['id'] = [util.add_org_prefix(id)]
        if request.args.get('blueprint_id'):
            bpid = request.args['blueprint_id']
            parameters['blueprint_id'] = [util.add_org_prefix(bpid)]
        if request.args.get('deployment_id'):
            did = request.args['deployment_id']
            parameters['deployment_id'] = [util.add_org_prefix(did)]
        response = requests.get(self.url + path,
                                params=parameters,
                                headers=self.headers)
        _check_exception(response)
        return json.loads(response.content)
