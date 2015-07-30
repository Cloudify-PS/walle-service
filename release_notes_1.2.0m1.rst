==============================
Score v1.2.0m1 release process
==============================

Release version: v1.2.0m1
Version Score tag URL: https://github.com/vcloudair/score-service/releases/tag/1.2.0m1
Version Score UI tag URL: https://github.com/vcloudair/vca.io/releases/tag/v1.2.0m1
Version description: This version stands for initial stable release.
Version release date: 30 July 2015
Version author(s):
    Konstantin Ilyashenko <konstantin@gigaspaces.com>
    Denys Makogon <Denys@gigaspaces.com>
    Paco Gomez <contact@pacogomez.com>
    Denis Makogon <lildee1991@gmail.com>
    Mykhailo Durnosvystov <Mikhail@gigaspaces.com>
    Denis Pauk <pauk.denis@gmail.com>
    yoramw <yoram@gigaspaces.com>


ChangeLog
=========

9a67318 (origin/master, origin/HEAD, master) Merge pull request #99 from GlaciErrDev/updating_real_mode_config
e53280c Merge pull request #108 from GlaciErrDev/SCOR-134_Support_ignore_live_nodes_for_deployments_delete
1e2892d fixes defauld value
2662c93 SCOR-134: Support ignore live nodes for deployments delete
60b6f39 Merge pull request #105 from kostya13/SCOR-137
4688560 SCOR-137 Style fix
eaa0e84 SCOR-137 Style fix
dd061bb SCOR-137 Refactoring
1ee589a SCOR-137 Check if json is empty or incorrect
474e2d9 SCOR-137 Update executions methods accorded to cloudify API.
1043bea SCOR-137 Update unittests
fd4187c SCOR-137  Start execution must use Executions class instead ExecutionsId
8de2841 Merge pull request #91 from kostya13/SCOR-121
8e79662 Merge pull request #104 from vcloudair/update-nginx-configuration-file
9f24539 Update nginx conf to reflect proper www location
8f6a5b9 Merge pull request #84 from denismakogon/SCOR-111
a5f9b89 Merge pull request #103 from vcloudair/denismakogon-patch-1
5181d08 Update initctl score config
4c4c560 Merge pull request #102 from vcloudair/fix-script-configure-score
de048bd fix-script-configure-score
d89a270 SCOR-121 Move function to util
5b66d1c (gh/SCOR-111) SCOR-107: Validate built-in plugins and workflows aren't used
12acea8 Merge pull request #101 from kostya13/SCOR-130
84d1a97 SCOR-130 Update score bluprints for new syntax of keypair node.
518dfe3 SCOR-121 Fix logic error
f6b8748 SCOR-121 Style fix
1ecec64 SCOR-121 Create separate function for add org prefix to org_id
689a20a SCOR-107: Implement fabric operation validation
d0a1e1a SCOR-109: Implement imports validation
099f0aa SCOR-106: Implement blueprint plugin validations
88c3dd5 SCOR-106: Implement blueprint plugin validations
efec45e SCOR-109: Remove hidden blueprints deletion
864d255 Merge pull request #97 from GlaciErrDev/Different_API_signatures_for_events
91732fc SCOR-109: Implemet file system imports check
3acd6f5 SCOR-109: Additional pre-parsing validation
b9c5561 SCOR-105: Fix stylechecks
1b3bef8 SCOR-105: Switch types.yaml location
630c422 Updating real mode test config
440360e SCOR-105: Implement blueprint plan checks
f7bc218 Adding post method into Events class
79a5bd1 Merge pull request #77 from kostya13/SCOR-102
69c1e42 SCOR-102 Remove comments
1b60f09 SCOR-105: Implement blueprint plan checks
3ef6d7c SCOR-104: Implement server-side blueprints validation
acd9b82 Merge pull request #96 from denismakogon/fix-docker
b0074c4 (gh/fix-docker) Fix outdated Dockerfile to reflect recent updates
f84c783 Merge pull request #95 from vcloudair/fix-types-yaml-mapping
d7373e5 Fix worker installer 'install' interface
b5af82b Merge pull request #94 from GlaciErrDev/retrying_login_to_vca_in_tests
35a2b8d Retrying login to vca in tests if it failed.
d6edbcf Merge pull request #93 from GlaciErrDev/moving_test_client_into_IntegrationBaseTestCase_class
6b8bef0 Moving flask test_client into IntegrationBaseTestCase
373e77e Merge pull request #87 from GlaciErrDev/Implement_real_mode_integration_testing_#2
2506134 Added handling case when developer passed incorrect parameters for login to VCS.
448d9ff SCOR-79: Implemented real mode integration testing
ab5c772 Merge pull request #92 from kostya13/master
95ff1f8 Fix requirements
f863fb6 SCOR-121 Add test for empty string
7ee6411 SCOR-121 Function add_org_prefix add prefix to empty object
4aab2bb SCOR-102 Style fixes
577ade6 Merge pull request #90 from denismakogon/fix-requirements
c69d45b (gh/fix-requirements) Fix requirements
c4ed60c Merge pull request #71 from kostya13/SCOR-72
d487dc9 Merge pull request #89 from vcloudair/update-nginx-path
a0fd405 Update nginx path
0056ac1 Merge pull request #79 from denismakogon/SCOR-71
5319b1e (gh/SCOR-71) SCOR-103: Add custom types.yaml for Score service
1ad878e Merge pull request #88 from vcloudair/fix-ect-to-etc
2bf26d4 Update configure.sh
2db426a Merge pull request #86 from kostya13/master
7328992 Fix Error 500 with expired token
d942703 Merge pull request #85 from vcloudair/apply-nginx-configuration
aa24bbc Update configure.sh
da911ba SCOR-72 Fix style
5471cbb SCOR-102 Add more checks for remove_org_prefix
091fdc3 SCOR-102 Add more tests.
2a58f1b Merge pull request #83 from vcloudair/add-input-for-start-lifecycle
25cd374 Update vcloud-score-blueprint.yaml
5e1e7f0 Merge pull request #82 from vcloudair/update-score-node-input
4ee7580 Update score node input
ee89ce4 Merge pull request #81 from vcloudair/remote-tmp
a61b16a Update configure.sh
26247bb Merge branch 'master' of https://github.com/vcloudair/score-service into SCOR-72
f9216a4 Merge pull request #75 from denismakogon/SCOR-82
3c149a1 SCOR-72 Improve validation.
1f63eef SCOR-72 Update swagger parameters description
b90f625 SCOR-82: Move python-bash to pure bash
6b42142 Update blueprints for score deb package
c8146ee Merge pull request #78 from denismakogon/master
fdb314d (gh/master) Fix oslo.utils to oslo_utils due to its deprecation
87972c2 SCOR-72 Update integration tests
68a6c98 SCOR-102 Update unittests
230e05d SCOR-102 Rever tests
4dda0b1 SCOR-72 Style fixes
ca70f18 SCOR-102 Skip removing org prefix from empty objects. Update tests.
a1629fb SCOR-72 Update integration test
fa94665 SCOR-72 Add more verbose error messages
a275be7 SCOR-102 Update unittests
e84ae1c SCOR-72 Update error messages
218c069 SCOR-102 Fix ececutions
eb940cd Merge branch 'SCOR-102' of https://github.com/kostya13/score-service into SCOR-102
a27470f SCOR-102 Fix return value for the events
8d4a2a7 SCOR-102 Incorrect id in "GET /blueprints/:id" response
25a0110 Merge pull request #76 from denismakogon/SCOR-101
a97b9a4 SCOR-102 Fix return value for the events
4558588 SCOR-102 Incorrect id in "GET /blueprints/:id" response
d9f924b (gh/SCOR-101) SCOR-101: Update PR according to given comments
bb7de9e SCOR-101 Fix integration tests
e9e488e SCOR-101 Add strict slashes flag
5b485ce SCOR-101 Add documentation for 'deployment_id'. Update unittests
51caa66 SCOR-101 Style fixes.
0b465b2 SCOR-101 Update unittests for utils
59cf5fe SCOR-101 Fix unittests
7cea019 SCOR-101 Fix filter logic
096cbe9 SCOR-101 Filter execution responses by org_id.
60065da SCOR-101 Fix execution command
2154753 Merge pull request #70 from kostya13/SCOR-95
2b2b9f2 Merge pull request #73 from GlaciErrDev/Update_swagger_documentation
b069180 Fixes typos
8115f58 Merge pull request #72 from kostya13/add_api
550ee59 SCOR-95 Add unittests
c941b77 Merge pull request #46 from kostya13/SCOR-81
908a989 SCOR-100: Updated swagger documentation for /blueprint command
39844a1 Change spaces to tabs
81d9000 Add path for swagger api documentation
d1dc019 SCOR-95 Refactoring
8cc88c7 SCOR-72 Bad request handle with exception
2ce1743 Merge pull request #66 from kostya13/SCOR-72
a12cada SCOR-95 Filter error message for deploymen creation from Org-ID that comes as part of deployment name
1029ce0 SCOR-72 Style fixes
2b65b9b Merge pull request #69 from denismakogon/fix-swagger-impl
79294e0 Fix swagger implementation
b78ac2b Merge pull request #68 from GlaciErrDev/remove_working_with_db
7392d65 Removed working with db via score_manage
e9a07e9 SCOR-72 Fix integration test
2ff326e SCOR-72 Style fixes
aec742b Merge pull request #65 from kostya13/fix_version
cf040c5 SCOR-72 Style fix
4e0ee9b Fix unit test
2d32c3d SCOR-72 Improve service detection logic
ecba6f0 SCOR-72 Improve login command. Add tests
21f9062 Delete error line
7299e8e Fix versions
0219940 Setup version of cloudify modules to 3.2
d0b4711 Merge pull request #64 from denismakogon/nginx-fix
fbfdd69 Add content size limitation to vca_io
2d7957a Merge pull request #63 from kostya13/fix_config
b4fb928 Fix nginx conf. Add /status command
0282432 Merge pull request #62 from denismakogon/fix-nginx-conf
580ea59 Fix nginx conf
45a9f1d Merge pull request #59 from kostya13/SCOR-23
2405177 SCOR-23 Add python-virtualenv to install
d1ff21d SCOR-23 Add git to install command
e44a7f5 SCOR-23 Provide deployment and configuration docs Update installation documentation
92306cd SCOR-72 Change method to POST. Set default values for parameters.
a30e9c1 Merge pull request #39 from denismakogon/SCOR-32
51a64b5 Added ability to choice mode via flag from commit message
ad86164 SCOR-32: Refactor integration tests
0aac43d Merge pull request #56 from kostya13/SCOR-72
835fdbf SCOR-72 Update variables names
d62b56c Merge pull request #54 from denismakogon/SCOR-84
9b129be SCOR-82: Switch from python-bash to pure bash
cfb9d4c SCOR-72 Update class with swagger meta information.
178c0c1 SCOR-72 Edit log message.
b746e1a Merge pull request #37 from GlaciErrDev/swagger_representation
6cc2e92 SCOR-72 Fix logic. Fix style.
2fdb107 Fixes typos
64303f0 Fixes typos, description and remove version from routs
46a5ecc SCOR-61: Added Swagger representation of the Score API
849eb58 Merge branch 'master' of https://github.com/vcloudair/score-service into SCOR-72
281e3ea SCOR-72 Style fix
14b17cb Merge pull request #55 from vcloudair/improve-logging
f675fb1 SCOR-68: Implement logging
c674a32 SCOR-72 Update return code
2374f15 SCOR-72 Add file.
1d0a37a SCOR-72 Create a "special" login verb for the Restful score service
aa2104d SCOR-68: Implement logging
47509af Merge pull request #53 from GlaciErrDev/added_execution_command_from_user
1315ca6 Added execution command from user
86ed8da Merge pull request #51 from denismakogon/extract-bash-script
ec555af SCOR-82: Switch from python-bash to pure bash
c05f868 Merge pull request #40 from denismakogon/SCOR-77
cf430ef (gh/SCOR-77) SCOR-77: Add local blueprint execution
2a816ca Merge pull request #50 from GlaciErrDev/fixes_exporting_env_variables
cab1548 Fixes exporting env variables
641a0f1 Merge pull request #49 from GlaciErrDev/fixes_upgrade_db
ee16529 Fixes upgrade db in score configure script
1261ac2 Merge pull request #47 from denismakogon/SCOR-68
392f3a5 SCOR-68: Add new variables to fabric scripts
02a8edf Merge pull request #42 from GlaciErrDev/fix_env_variables
0672c4c Merge pull request #48 from denismakogon/extract-bash-script
323882e Move from python-bash scripts to pure bash scripts
12945d2 Merge pull request #45 from GlaciErrDev/fixes_score_postgres_script
b7f98b5 Merge pull request #44 from denismakogon/SCOR-68
b989d8a SCOR-68: Implement logging
a7d7cb2 SCOR-81 network_use_existing: fasle - doesn't wrok
0433c05 Fixes install_score_postgresql script
efee07d SCOR-68: Implement logging
ba96e1a Merge pull request #43 from denismakogon/fix-serialization
5499872 (gh/fix-serialization) Fix serialization problems at API site
8ebd3bd Fixes SCORE_DB variable in env
a6a3ec3 Merge pull request #41 from denismakogon/SCOR-68
85b7d13 SCOR-68: Implement logging for Score
e340cbd Merge pull request #38 from GlaciErrDev/fix_credential_issues_for_postgres
9577c55 Fixes creating db with credentials from inputs
ead445f Merge pull request #30 from denismakogon/fix-migration-with-org-id-feature
d7e9081 (gh/fix-migration-with-org-id-feature) SCOR-62: Address minor comments for deployment resources
50f3451 SCOR-32: Add install worklow to local blueprint. Stage 2
b664958 SCOR-32: Add install worklow to local blueprint. Stage 1
c33cd63 SCOR-32: Add blueprint upload integration tests
a3314af SCOR-32: Refactor .travis.yml
5d1528a SCOR-62: Add Org-ID limits. Stage 3
9e05906 SCOR-62: Add Org-ID limits. Stage 2
cc606f0 SCOR-62: Add Org-ID limits
ee934f2 Merge pull request #34 from denismakogon/code-review-policy
daec243 Merge pull request #36 from denismakogon/master
0da33bf Fix blueprints that are not passing required checks
a3a35fd Merge pull request #35 from denismakogon/master
6545a3c Fix Travis.yaml
6df4267 Merge pull request #32 from GlaciErrDev/pastgres_score_diff_nodes
e2598a2 Fixes postgres errors
00cbccc (gh/code-review-policy) Add code review policy
66b14ee Merge pull request #33 from denismakogon/master
7c53159 Fix PEP8 issue in app.py
58bd988 Merge pull request #31 from denismakogon/master
aa6cab8 Remove arg parsing from app.py
3d74785 Merge pull request #27 from kostya13/SCOR-60
53c6b1c Merge pull request #29 from denismakogon/add-ids-to-initsql
3719d51 (gh/add-ids-to-initsql) Add IDs (UUID) to init.sql
5a98bfc Merge pull request #28 from denismakogon/fix-migration-with-org-id-feature
4973c19 SCOR-52: Add info field to Org-ID model
d1bd0e5 SCOR-52 - Fix migrations according to LB plans
b39d5f3 Merge pull request #26 from 0lvin/a_lot_fixes
5571dc7 Add ability to start with postgresql into score blueprint
54cac39 SCOR-60 create 'status' api call to return version and status of the service
da61033 Move test_executions.py to another folder
fe6293b Merge branch 'kostya13-SCOR-56'
e99ff43 Merge branch 'SCOR-56' of https://github.com/kostya13/score-service into kostya13-SCOR-56
7861a81 Merge pull request #22 from denismakogon/testing-env
f695a05 Merge pull request #21 from vcloudair/SCOR-52
90abe81 SCOR-52: add org_info
5682900 Merge branch 'SCOR-52' of github.com:0lvin/score-service into SCOR-52
b6b2101 Merge remote-tracking branch 'base/master' into SCOR-52
0868c36 SCOR-56 Style fix
2912316 Merge pull request #25 from GlaciErrDev/fix_string
84aee44 Fix string in configure script
89b5e46 SCOR-56 Change test library
b0c2e6a Merge pull request #24 from GlaciErrDev/Fix_version
d8d63b5 Fix version
04c8ce8 SCOR-56 Implement cancel workflow execution on score, pyvcloud and vca-cli
0c0b9cc SCOR-56 Implement cancel workflow execution on score, pyvcloud and vca-cli Add unit tests
042430b SCOR-52: test travis postgres install
d7ad485 SCOR-52: add enable/disable organization code with tests
dd69e9f (gh/testing-env) SCOR-32: Add more local blueprints
e123716 SCOR-52: add enable/disable organization code with tests



Components for Score v1.2.0m1
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


Requirements for Score v1.2.0m1
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


Testing requirements for Score v1.2.0m1
=======================================

hacking>=0.10.0,<0.11
mock>=1.0
nose>=1.3
coverage
fabric==1.8.3
testtools>=0.9.36,!=1.2.0
gitpython


External dependencies/requirements for Score v1.2.0m1
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

tosca-vcloud-plugin==1.2
cloudify-fabric-plugin==1.2

Tag URLs::

    https://github.com/cloudify-cosmo/cloudify-fabric-plugin/releases/tag/1.2
    https://github.com/cloudify-cosmo/tosca-vcloud-plugin/releases/tag/1.2


========
Security
========

Score v1.2.0 support blueprints security validations::

    custom Score types available at http://s3.amazonaws.com/vcloud-score/types.yaml
    server-side blueprint validation
    no groups, no policy types or triggers are allowed to be used.
    validation for supported plugins
    built-in workflows validation
    blueprints imports validation
    fabric environment configuration validation

See more at https://cloudify.hackpad.com/SCORE-DSL-Validation-FqexVSF6CDv#:h=DSL-Validations


