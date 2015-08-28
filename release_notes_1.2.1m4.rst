=============================
Score 1.2.1m4 release process
=============================

Release version: v1.2.1m4
Version Score tag URL: https://github.com/vcloudair/score-service/releases/tag/1.2.1m4
Version Score UI tag URL: https://github.com/vcloudair/vca.io/releases/tag/v1.2.1m4
Version description: More strict validation inputs and use fabric plugin fork.
Version release date: 27 August 2015
Version author(s):
    Konstantin Ilyashenko <konstantin@gigaspaces.com>
    Denys Makogon <Denys@gigaspaces.com>
    Paco Gomez <contact@pacogomez.com>
    Denis Pauk <pauk.denis@gmail.com>
    Mykhailo Durnosvystov <Mikhail@gigaspaces.com>
    yoramw <yoram@gigaspaces.com>
    Vladimir Antonovich <Vladimir-Antonovich@users.noreply.github.com>


ChangeLog for 1.2.1m4
=====================

6ac98b8 Merge pull request #179 from GlaciErrDev/filtering_event_messages
1f8c4e0 SCOR-194: Filtered message in events
3f701bc Merge pull request #175 from GlaciErrDev/Implement_instance_list_of_account
d7bbc8f SCOR-184: Expanded reply from route `/login`
412ffc4 SCOR-184: Implement instance list of account
26f7559 Merge pull request #169 from Vladimir-Antonovich/SCOR-174
c1df245 Delete vca_io
f697fee Merge pull request #174 from kostya13/SCOR-201
3d69567 SCOR-201 Use enviroment variable in testing framework for configuration file.
7487119 Merge branch 'master' of https://github.com/vcloudair/score-service
638a8a1 Fix delete org-ids
d9c8464 add su root root - new file owners
9f64b43 Fix syntax errors
165b19d Merge pull request #170 from denismakogon/SCOR-181
70d446c SCOR-181: Filter execution on GET request for /executions/<id>
3c423b6 Parameter is_production: has been added in to blueprint to select how to do deployment. Now configure.sh creates config files and scripts to make logrotate and send reports.
6c0b401 SCOR-174
f1f2d81 Merge pull request #167 from denismakogon/SCOR-188
6caeeed SCOR-188: Disable HTTP access to Score

Components for Score v1.2.1m4
=============================


    +------------------+---------+
    | Name             | Version |
    +------------------+---------+
    | Cloudify Manager |  3.2.1  |
    +------------------+---------+
    |       Nginx      |  1.4.6  |
    +------------------+---------+
    |      Gunicorn    | 19.3.0  |
    +------------------+---------+


Requirements for Score v1.2.1m4
===============================


Common stack
------------

pbr>=0.11,<2.0
Flask==0.10.1
flask-restful==0.2.12
flask-restful-swagger==0.12
requests==2.4.3
PyYAML==3.10
pyvcloud==14
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


Testing requirements for Score v1.2.1m4
=======================================

hacking>=0.10.0,<0.11
mock>=1.0
nose>=1.3
coverage
fabric==1.8.3
testtools>=0.9.36,!=1.2.0
gitpython
tox


External dependencies/requirements for Score v1.2.1m4
=====================================================

VMware stack
------------

pyvcloud 14
vca-cli 14
vca.io 1.2.1m4

================
Approved plugins
================

Cloudify stack
--------------

tosca-vcloud-plugin in (1.2, 1.2.1, 1.2.1m2, 1.2.1m3, 1.2.1m4)
cloudify-fabric-plugin==1.2 (our fork only)
custom cloudify-script-plugin 1.2.1m1

Tag URLs::

    http://s3.amazonaws.com/vcloud-score/cloudify-fabric-plugin-1.2.zip

    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m2
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m3
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m4

    https://github.com/vcloudair/cloudify-script-plugin/releases/tag/1.2.1m1

========
Security
========

Score v1.2.1m4 improved security by:
    * Disable HTTP access to Score
    * Filter execution on GET request for /executions/<id>
