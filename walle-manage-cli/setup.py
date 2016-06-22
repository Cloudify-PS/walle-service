########
# Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
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
    name='walle-manage-cli',
    version='1.0',
    author='Gigaspaces',
    author_email='cosmo-admin@gigaspaces.com',
    packages=['walle_manage_cli'],
    license='LICENSE',
    description='CLI for Score service management',
    entry_points={
        'console_scripts': [
            'walle-manage-cli = walle_manage_cli.cli:main']
    },
    install_requires=[
        'cloudify-dsl-parser',
        'click'
    ]
)
