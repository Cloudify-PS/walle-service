import json
import pkgutil
from flask import Flask


def get_version():
    version_data = get_version_data()
    return version_data['version']


def get_version_data():
    data = pkgutil.get_data('score_api_server', 'VERSION')
    return json.loads(data)
    
