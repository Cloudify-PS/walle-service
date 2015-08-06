===============================
Score v1.2.1m1 release process
===============================

Release version: v1.2.1m1
Version Score tag URL: https://github.com/vcloudair/score-service/releases/tag/1.2.1m1
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

ChangeLog for v1.2.1m1
=======================

c96992c Merge pull request #129 from vcloudair/SCOR-158
4ab8aac SCOR-158: enable plugin checks
73d60bc Merge pull request #127 from kostya13/tox
02693a9 Add tox to test-requirements
b063f5c Merge pull request #125 from vcloudair/SCOR-157
5ddfc2f SCOR-157: use key content instead key_file in postrgesql blueprints
2721d91 Merge pull request #113 from denismakogon/SCOR-135
6d50833 Merge pull request #112 from kostya13/SCOR-115
8cbe30e SCOR-115: Apply JSON schema validation to all requests across Score resources
a805553 Merge pull request #123 from denismakogon/remote-uniq-flags-from-plugins
70a0d01 Merge pull request #121 from kostya13/SCOR-155
485e4f7 SCOR-155: Events List page always shows only 10 first events
aaf3301 Make approved plugin name and plugin source non-uniq
892f1c6 Merge pull request #122 from vcloudair/update-tosca-source
eb8d41d Update TOSCA plugin version
033a0b7 Merge pull request #115 from kostya13/SCOR-98
1a42ac3 SCOR-135: Implement post-deployment checks
8ebc865 Merge pull request #109 from GlaciErrDev/Different_API_signatures_for_events
740d541 Merge pull request #120 from GlaciErrDev/Updating_real_mode_test_config
60146ce Updating real mode test config
7eb837c SCOR-124: Made functionality for deployment and execution in integration tests
ff1c9d5 Merge pull request #119 from denismakogon/fix-delete-deployment
d5942f3 Improve response filtering
776b60d Merge pull request #116 from kostya13/master
822b2ab Fix unittests
5a15440 Merge pull request #117 from vcloudair/SCOR-149
4b23254 SCOR-149: temporary disable key_file check
5a651f2 SCOR-98 Add tests, update swagger description
78f26a5 Change default url for ondemand service
129bea2 SCOR-98 Add command  GET /deployments/{deployment_id}/outputs to get deployment outputs

Components for Score v1.2.1m1
=============================


    +------------------+---------+
    | Name             | Version |
    +------------------+---------+
    | Cloudify Manager |   3.2   |
    +------------------+---------+
    |       Nginx      |   1.9   |
    +------------------+---------+
    |      Gunicorn    | 19.3.0  |
    +------------------+---------+


Requirements for Score v1.2.1m1
===============================


Common stack
------------

pbr>=0.11,<2.0
Flask==0.10.1
flask-restful==0.2.12
flask-restful-swagger==0.12
requests==2.4.3
PyYAML==3.10
pyvcloud>=13rc13
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

cloudify-rest-client==3.2
cloudify-dsl-parser==3.2


Testing requirements for Score v1.2.1m1
=======================================

hacking>=0.10.0,<0.11
mock>=1.0
nose>=1.3
coverage
fabric==1.8.3
testtools>=0.9.36,!=1.2.0
gitpython
tox


External dependencies/requirements for Score v1.2.1m1
=====================================================

VMware stack
------------

pyvcloud==14rc6
vca-cli==13
vca.io

================
Approved plugins
================

Cloudify stack
--------------

tosca-vcloud-plugin in (1.2, 1.21)
cloudify-fabric-plugin==1.2 (our fork only)

Tag URLs::

    http://s3.amazonaws.com/vcloud-score/cloudify-fabric-plugin-1.2.zip
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1

========
Security
========

Score v1.2.1m1 improved security validations in such way:
    * usage of fabric plugin limited to our version of fabric from
    http://s3.amazonaws.com/vcloud-score/cloudify-fabric-plugin/1.2/plugin.yaml
    * more strict json validation.
