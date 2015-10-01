=============================
Score 1.2.1m5 release process
=============================

Release version: v1.2.1m5
Version Score tag URL: https://github.com/vcloudair/score-service/releases/tag/1.2.1m5
Version Score UI tag URL: https://github.com/vcloudair/vca.io/releases/tag/v1.2.1m5
Version description: Improve security and testing
Version release date: 3 October 2015
Version author(s):
    Konstantin Ilyashenko <konstantin@gigaspaces.com>
    Denys Makogon <Denys@gigaspaces.com>
    Paco Gomez <contact@pacogomez.com>
    Denis Pauk <pauk.denis@gmail.com>
    Mykhailo Durnosvystov <Mikhail@gigaspaces.com>
    yoramw <yoram@gigaspaces.com>
    Vladimir Antonovich <Vladimir-Antonovich@users.noreply.github.com>


ChangeLog for 1.2.1m5
=====================
4c78c18 Merge pull request #192 from GlaciErrDev/update_jmeter_testplan
5eb187b Updated jmeter test plan
f501351 Merge pull request #191 from GlaciErrDev/using_existing_nginx_node
0d726e9 Using existing nginx node
47f57de Merge pull request #190 from vcloudair/SCOR-193
148884a SCOR-193: add 1.2.1m5 releases
b57a8fb Merge pull request #189 from vcloudair/Fix_score_ui_section
963d3d8 Update vcloud-score-blueprint.yaml
25a1085 Merge pull request #188 from vcloudair/fix_nginx_fabric_env
cb8e5fc Fix port for score_ui fabric_env in blueprint
c6beb04 Merge pull request #187 from kostya13/SCOR-198
44a440e SCOR-198 Whitelist vcloud_org_url
2baf43a Merge pull request #186 from vcloudair/SCOR-200
cb4658d SCOR-200: use ubuntu as user for run gunicorn
7c5392f Merge pull request #180 from vcloudair/SCOR-190
4989f00 SCOR-190: add file with Diffie Hellman params
f7a3b53 Merge pull request #176 from denismakogon/decouple-deployment-score
863a0e9 Merge pull request #183 from denismakogon/make-auth-requests-more-parse-friendly
5a54bc6 Decouple Score nodes
18b8f4f Make more safe authorization within UI
49e2d3c Merge pull request #181 from GlaciErrDev/requests_instead_of_urllib
ada797d SCOR-202: Used Python requests instead of urllib
4cbdc59 Merge pull request #177 from denismakogon/SCOR-39
70e1e49 SCOR-39: Download blueprint API feature


Components for Score v1.2.1m5
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


Requirements for Score v1.2.1m5
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


Testing requirements for Score v1.2.1m5
=======================================

hacking>=0.10.0,<0.11
mock>=1.0
nose>=1.3
coverage
fabric==1.8.3
testtools>=0.9.36,!=1.2.0
gitpython
tox


External dependencies/requirements for Score v1.2.1m5
=====================================================

VMware stack
------------

pyvcloud 14
vca-cli 14
vca.io 1.2.1m5

================
Approved plugins
================

Cloudify stack
--------------

tosca-vcloud-plugin in (1.2, 1.2.1, 1.2.1m2, 1.2.1m3, 1.2.1m4, 1.2.1m5)
cloudify-fabric-plugin==1.2 (our fork only)
custom cloudify-script-plugin 1.2.1m1

Tag URLs::

    http://s3.amazonaws.com/vcloud-score/cloudify-fabric-plugin-1.2.zip

    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m2
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m3
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m4
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2.1m5

    https://github.com/vcloudair/cloudify-script-plugin/releases/tag/1.2.1m1

========
Security
========

Score v1.2.1m5 improved security by:
    * Whitelist for vcloud_org_url
    * Run Python on the score server as non-root user
    * Delete SSH keys after install workflow
    * Update SSL Configuration on Nginx 
    * Use Python requests instead of urllib 
