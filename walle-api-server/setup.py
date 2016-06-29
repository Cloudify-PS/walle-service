########
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from setuptools import setup

setup(
    name='walle-service',
    version='1.4rc1',
    author='VMware, Gigaspaces',
    author_email='cosmo-admin@gigaspaces.com',
    packages=[
        'walle_api_server',
        'walle_api_server/cli',
        'walle_api_server/common',
        'walle_api_server/db',
        'walle_api_server/resources'
    ],
    license='License :: OSI Approved :: Apache Software License',
    description='Walle service',
    entry_points={
        'console_scripts': [
            'walle-service = walle_api_server.cli.app:main',
            'walle-manage = walle_api_server.cli.manage:main'
        ]
    },
    install_requires=[
        'pbr>=0.11,<2.0',
        'Flask==0.10.1',
        'flask-restful==0.2.12',
        'flask-restful-swagger==0.12',
        'requests==2.7.0',
        'PyYAML==3.10',
        'pyvcloud>=15rc1',
        'cloudify-rest-client==3.4a4',
        'cloudify-dsl-parser==3.4a4',
        'oslo.config',
        'psycopg2',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'oslo.utils',
        'PrettyTable>=0.7,<0.8',
        'functools32',
        'jsonschema',
        'python-keystoneclient'
    ],
    classifiers=[
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ]
)
