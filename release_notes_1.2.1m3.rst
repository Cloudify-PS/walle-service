==============================
Score v1.2.1m3 release process
==============================

Release version: v1.2.1m3
Version Score tag URL: https://github.com/vcloudair/score-service/releases/tag/1.2.1m3
Version Score UI tag URL: https://github.com/vcloudair/vca.io/releases/tag/v1.2.1m3
Version description: More strict validation inputs and use fabric plugin fork.
Version release date: 06 August 2015
Version author(s):
    Konstantin Ilyashenko <konstantin@gigaspaces.com>
    Denys Makogon <Denys@gigaspaces.com>
    Paco Gomez <contact@pacogomez.com>
    Denis Pauk <pauk.denis@gmail.com>
    Mykhailo Durnosvystov <Mikhail@gigaspaces.com>
    yoramw <yoram@gigaspaces.com>
    Vladimir Antonovich <Vladimir-Antonovich@users.noreply.github.com>

ChangeLog for v1.2.1m3
======================

90c67b4 (HEAD, origin/master, origin/HEAD, release-1.2.1m3, master) Change order of server_name parameter
66c3712 Merge pull request #158 from vcloudair/nginx-redirect
66c3712 (HEAD, origin/master, origin/HEAD, release-1.2.1m3, master) Merge pull request #158 from vcloudair/nginx-redirect
bdd014f Merge pull request #156 from vcloudair/logrotate-for-score-api.log
20d4f76 Update configure.sh
ca66f73 Add logorotate for score-api.log
9351fd2 Merge pull request #159 from kostya13/SCOR-173
3c80976 Merge pull request #162 from yoramw/cfy-mgr-bp
346e3cb updated agent package with a new agent package that includes the score script plugin
39330e6 Merge pull request #149 from yoramw/cfy-mgr-bp
ec3bc42 Merge pull request #142 from denismakogon/make-score-blueprint-to-work-with-existing-prostresql
7673682 Update configure.sh
5fe77a2 SCOR-173 Add limits checks
4c5d313 SCOR-175: stage/prod vca_io nginx
535a8bf remove }
600e230 Merge pull request #160 from denismakogon/add-more-executions
ca15a5f Merge pull request #161 from denismakogon/improve-logging-as-proof-of-internal-data-filtering
f20e1ae (gh/improve-logging-as-proof-of-internal-data-filtering, improve-logging-as-proof-of-internal-data-filtering) Improve logging as proof of internal data filtering
1dc98b6 (gh/add-more-executions, add-more-executions) Add safe script runner to special cases
5ca7c4a SCOR-173 Login with unauthorized user does not give any meaningful error message
986f9e9 SCOR-175: nginx redirects to HTTPS
9f45ddb Merge pull request #157 from denismakogon/make-auth-requests-more-parse-friendly
817b3ee (gh/make-auth-requests-more-parse-friendly, make-auth-requests-more-parse-friendly) Improve logging for auth requests v2
987f3e0 Update configure.sh
9231799 Merge pull request #155 from denismakogon/make-auth-requests-more-parse-friendly
8cde6ac Improve logging for auth requests
2399f48 (gh/make-score-blueprint-to-work-with-existing-prostresql, make-score-blueprint-to-work-with-existing-prostresql) Use existing resource node for postgresql if needed
e4add85 Merge pull request #154 from denismakogon/improve-blueprint-archive-structure-validation
0c75f1a (gh/improve-blueprint-archive-structure-validation, improve-blueprint-archive-structure-validation) Improve blueprint structure validation


Components for Score v1.2.1m3
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


Requirements for Score v1.2.1m3
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


Testing requirements for Score v1.2.1m3
=======================================

hacking>=0.10.0,<0.11
mock>=1.0
nose>=1.3
coverage
fabric==1.8.3
testtools>=0.9.36,!=1.2.0
gitpython
tox


External dependencies/requirements for Score v1.2.1m3
=====================================================

VMware stack
------------

pyvcloud 14
vca-cli 14
vca.io 1.2.1m3

================
Approved plugins
================

Cloudify stack
--------------

tosca-vcloud-plugin in (1.2, 1.2.1, 1.2.1m2, 1.2.1m3)
cloudify-fabric-plugin==1.2 (our fork only)
custom cloudify-script-plugin 1.2.1m1

Tag URLs::

    http://s3.amazonaws.com/vcloud-score/cloudify-fabric-plugin-1.2.zip

    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m2
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m3

    https://github.com/vcloudair/cloudify-script-plugin/releases/tag/1.2.1m1

========
Security
========

Score v1.2.1m3 improved security validations in such way:
    * usage of fabric plugin limited to our version of fabric from
    http://s3.amazonaws.com/vcloud-score/cloudify-fabric-plugin/1.2/plugin.yaml
    * more strict json validation.
