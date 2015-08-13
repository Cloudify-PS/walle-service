==============================
Score v1.2.1m2 release process
==============================

Release version: v1.2.1m2
Version Score tag URL: https://github.com/vcloudair/score-service/releases/tag/1.2.1m2
Version Score UI tag URL: https://github.com/vcloudair/vca.io/releases/tag/v1.2.1m1
Version description: More strict validation inputs and use fabric plugin fork.
Version release date: 06 August 2015
Version author(s):
    Konstantin Ilyashenko <konstantin@gigaspaces.com>
    Denys Makogon <Denys@gigaspaces.com>
    Paco Gomez <contact@pacogomez.com>
    Denis Pauk <pauk.denis@gmail.com>
    Mykhailo Durnosvystov <Mikhail@gigaspaces.com>
    yoramw <yoram@gigaspaces.com>

ChangeLog for v1.2.1m2
======================

61ce5d9 (HEAD, origin/master, origin/HEAD, master) Merge pull request #144 from kostya13/test-token
e43a9c6 SCOR-57: use our common valid blueprint without token
7339987 test token authentication
fb8f87f Merge pull request #150 from vcloudair/SCOR-161_1.2.1m2
70daea8 SCOR-161: update to 1.2.1m2
486d8d5 Merge pull request #143 from kostya13/SCOR-57
45e8ef4 SCOR-57: code cleanups
0191fbc SCOR-57 Change install to uninstall
2fd70d0 SCOR-57 Change workflow names
d116614 SCOR-57 Update special cases for new workflows
2ff22e5 SCOR-57 Convert workflow names
fc97999 SCOR-57 Allow vcloud-plugin to use vcloud token to perform operations
47dbf91 Merge pull request #148 from denismakogon/fix-travis.yml
72b5681 Merge pull request #145 from GlaciErrDev/Add_jmeter_test_plan
4889218 Merge pull request #147 from denismakogon/SCOR-167
cfef140 Merge pull request #146 from denismakogon/extend_logging_message
8f67831 Added the initial scenario for load testing script
493a550 Merge pull request #141 from denismakogon/add-approved-plugins-to-score-configuration
338bfeb update versions to 3.2.1
1691891 Merge pull request #106 from denismakogon/SCOR-139
2a5d3d1 Merge pull request #107 from denismakogon/SCOR-82
762a47f Merge pull request #140 from denismakogon/implement-blueprint-url-support
d3c5905 Merge pull request #138 from vcloudair/SCOR-162
4e23dc4 SCOR-162: cleanup blueprints
fed4549 Merge pull request #137 from kostya13/blueprint
8a0c561 Simple blueprint for integration tests
87821c0 Merge pull request #128 from kostya13/SCOR-98
16eb0c9 Merge pull request #134 from kostya13/SCOR-115
2fbfbbf SCOR-115 Use json object as input for deployments Fix integration tests.
a422a37 Merge pull request #133 from denismakogon/fix-deployment-limits
4e288e9 Fix deployment limits validation
7fc0fe3 SCOR-98 Implement REST API additions. Uploading ZIP files


Components for Score v1.2.1m2
=============================


    +------------------+---------+
    | Name             | Version |
    +------------------+---------+
    | Cloudify Manager |  3.2.1  |
    +------------------+---------+
    |       Nginx      |   1.9   |
    +------------------+---------+
    |      Gunicorn    | 19.3.0  |
    +------------------+---------+


Requirements for Score v1.2.1m2
===============================


Common stack
------------

pbr>=0.11,<2.0
Flask==0.10.1
flask-restful==0.2.12
flask-restful-swagger==0.12
requests==2.4.3
PyYAML==3.10
pyvcloud #latest
oslo.config
psycopg2
Flask-SQLAlchemy
Flask-Migrate
oslo.utils
PrettyTable>=0.7,<0.8
functools32
jsonschema

Cloudify stack
--------------

cloudify-rest-client==3.2.1
cloudify-dsl-parser==3.2.1


Testing requirements for Score v1.2.1m2
=======================================

hacking>=0.10.0,<0.11
mock>=1.0
nose>=1.3
coverage
fabric==1.8.3
testtools>=0.9.36,!=1.2.0
gitpython
tox


External dependencies/requirements for Score v1.2.1m2
=====================================================

VMware stack
------------

pyvcloud (latest)
vca-cli (latest)
vca.io (latest)

================
Approved plugins
================

Cloudify stack
--------------

tosca-vcloud-plugin in (1.2, 1.2.1, 1.2.1m2)
cloudify-fabric-plugin==1.2 (our fork only)

Tag URLs::

    http://s3.amazonaws.com/vcloud-score/cloudify-fabric-plugin-1.2.zip
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m2

========
Security
========

Score v1.2.1m2 improved security validations in such way:
    * usage of fabric plugin limited to our version of fabric from
    http://s3.amazonaws.com/vcloud-score/cloudify-fabric-plugin/1.2/plugin.yaml
    * more strict json validation.
