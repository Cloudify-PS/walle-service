====================
vCloud Walle service
====================

==========
Deployment
==========

.. code-block:: bash
    $ sudo apt-get install git postgresql-common libpq-dev
    $ sudo apt-get install libxml2-dev libxslt1-dev python-virtualenv python-dev
    $ git clone http://github.com/vcloudair/walle-service.git
    $ cd walle-service/walle-api-server/
    $ virtualenv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
    $ python setup.py install


=====
Usage
=====

Before run call db update/creation by::
.. code-block:: bash


    $ export WALLE_DB="sqlite:////tmp/walle-service.db"
    $  walle-manage db upgrade


Also WALLE_DB can be postgresql://walle:secret-password@localhost/walle
Once you will accomplish deployment guide your environment will have next CLI tool::

    walle-server
    walle-manage

Usage examples::
.. code-block:: bash

    $ export WALLE_HOST="0.0.0.0"; \
      export WALLE_PORT="5000"; \
      export WALLE_WORKERS="4";\
      export WALLE_LOGGING_LEVEL=INFO \
      export WALLE_LOGGING_FILE="/var/log/walle.api" \
      export WALLE_DB="sqlite:////tmp/walle-service.db"; \
      walle-server

      * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

====================
Gunicorn integration
====================

To run walle-server app under gunicorn please use this command
.. code-block::bash

    $ pip install gunicorn
    $ gunicorn -h

        usage: gunicorn [OPTIONS] [APP_MODULE]


Usage examples::
.. code-block:: bash


    $ export WALLE_HOST="0.0.0.0"; \
      export WALLE_PORT="5000"; \
      export WALLE_WORKERS="4"; \
      export WALLE_DB="sqlite:////tmp/walle-service.db"; \
      export WALLE_LOGGING_LEVEL=INFO \
      export WALLE_LOGGING_FILE="/var/log/walle.api"

    $ gunicorn -w ${WALLE_WORKERS} -b ${WALLE_HOST}:${WALLE_PORT} walle_api_server.cli.app:main

            [2015-06-09 13:11:34 +0000] [27905] [INFO] Starting gunicorn 19.3.0
            [2015-06-09 13:11:34 +0000] [27905] [INFO] Listening at: http://0.0.0.0:5000 (27905)
            [2015-06-09 13:11:34 +0000] [27905] [INFO] Using worker: sync
            [2015-06-09 13:11:34 +0000] [27916] [INFO] Booting worker with pid: 27916
            [2015-06-09 13:11:34 +0000] [27917] [INFO] Booting worker with pid: 27917
            [2015-06-09 13:11:34 +0000] [27918] [INFO] Booting worker with pid: 27918
            [2015-06-09 13:11:34 +0000] [27919] [INFO] Booting worker with pid: 27919


=============
Configuration
=============

Once you would like to change default Walle API server host/port and Cloudify manager
host/port to connect to you will need to create a configuration file for walle-server.
Configuration environment variables might have next look::
.. code-block:: bash


    $ export WALLE_HOST="0.0.0.0"
    $ export WALLE_PORT="5000"
    $ export WALLE_WORKERS="4"
    $ export WALLE_DB="sqlite:////tmp/walle-service.db"
    $ export WALLE_LOGGING_LEVEL=INFO
    $ export WALLE_LOGGING_LEVEL=INFO


==============
Administration
==============

New CLI tool 'walle-manage' does allow to add new Org-ID during Walle service runtime.
Here's an example of you can use this tool::
.. code-block:: bash


    $ walle-manage org-ids

        usage: Performs action related to Org-IDs

        Performs action related to Org-IDs

        positional arguments:
          {add,list,delete}
            add              Adds Org-ID.
            list             Lists Org-IDs.
            delete           Deletes Org-ID.

        optional arguments:
          -?, --help         show this help message and exit



    $ walle-manager org-ids add \
            --org-id 4174a0c7-cd86-4dc8-a784-2cb5b852e823 \
            --db-uri sqlite:////tmp/walle.db
            --info "test Org-ID"

        +----------+--------------------------------------+
        | Property | Value                                |
        +----------+--------------------------------------+
        | id       | 32ba94e2-b1bc-4b21-90e6-ca1e98c7335d |
        | info     | test Org-ID                          |
        | org_id   | 4174a0c7-cd86-4dc8-a784-2cb5b852e823 |
        +----------+--------------------------------------+



    $ walle-manage org-ids delete --org-id 4174a0c7-cd86-4dc8-a784-2cb5b852e823 --db-uri sqlite:////tmp/walle.db

        OK


    $ walle-manage org-ids list --db-uri sqlite:////tmp/walle.db

        +--------------------------------------+--------------------------------------+-------------+
        | ID                                   | Org ID                               | Info        |
        +--------------------------------------+--------------------------------------+-------------+
        | cc6dcf64-eaaf-47ee-a9a0-0baca81b4df0 | fc3f6e85-a818-407e-b6e6-5f8098f1d8ff | test Org-ID |
        +--------------------------------------+--------------------------------------+-------------+


    $ walle-manage org-id-limits

        usage: Performs action related to Org-ID limits

        Performs action related to Org-ID limits

        positional arguments:
          {create,list,update,delete}
            create              Creates deployment limits pinned to specific Org-ID
                                and specific Cloudify Manager
            list                Lists all Org-ID limits.
            update              Updates Org-ID limits with given keys by its ID.
            delete              Deletes Org-ID limit by its ID.

        optional arguments:
          -?, --help            show this help message and exit


    $ walle-manage org-id-limits create --org-id 07c41213-608a-4970-aef6-4c8819f964ca \
        --cloudify-host 127.0.0.1 \
        --cloudify-port 80 \
        --deployment-limits 100 \
        --db-uri sqlite:////tmp/walle.db

        +-----------------------+--------------------------------------+
        | Property              | Value                                |
        +-----------------------+--------------------------------------+
        | cloudify_host         | 127.0.0.1                            |
        | cloudify_port         | 80                                   |
        | created_at            | 2015-07-03 12:08:03.914647           |
        | deployment_limits     | 100                                  |
        | id                    | 38d71fe2-eb31-44f3-9dcd-d71feacf50cb |
        | number_of_deployments | 0                                    |
        | org_id                | 07c41213-608a-4970-aef6-4c8819f964ca |
        | updated_at            | 2015-07-03 12:08:03.914656           |
        +-----------------------+--------------------------------------+


    $ walle-manage org-id-limits list --db-uri sqlite:////tmp/walle.db

        +--------------------------------------+--------------------------------------+---------------+---------------+-------------------+-----------------------+----------------------------+----------------------------+
        | ID                                   | Org ID                               | Cloudify Host | Cloudify Port | Deployment Limits | Number Of Deployments | Created At                 | Updated At                 |
        +--------------------------------------+--------------------------------------+---------------+---------------+-------------------+-----------------------+----------------------------+----------------------------+
        | 38d71fe2-eb31-44f3-9dcd-d71feacf50cb | 07c41213-608a-4970-aef6-4c8819f964ca | 127.0.0.1     | 80            |               100 |                     0 | 2015-07-03 12:08:03.914647 | 2015-07-03 12:08:03.914656 |
        +--------------------------------------+--------------------------------------+---------------+---------------+-------------------+-----------------------+----------------------------+----------------------------+


    $ walle-manage org-id-limits update --id 38d71fe2-eb31-44f3-9dcd-d71feacf50cb --deployment-limits -1 --db-uri sqlite:////tmp/walle.db


        +-----------------------+--------------------------------------+
        | Property              | Value                                |
        +-----------------------+--------------------------------------+
        | cloudify_host         | 127.0.0.1                            |
        | cloudify_port         | 80                                   |
        | created_at            | 2015-07-03 12:08:03.914647           |
        | deployment_limits     | -1                                   |
        | id                    | 38d71fe2-eb31-44f3-9dcd-d71feacf50cb |
        | number_of_deployments | 0                                    |
        | org_id                | 07c41213-608a-4970-aef6-4c8819f964ca |
        | updated_at            | 2015-07-03 12:10:32.524507           |
        +-----------------------+--------------------------------------+

    $ walle-manage approved-plugins add --name fabric --source https://github.com/cloudify-cosmo/cloudify-fabric-plugin/archive/1.2.zip --type deployment_plugins --db-uri sqlite:////tmp/walle.db


        +-------------+--------------------------------------------------------------------------+
        | Property    | Value                                                                    |
        +-------------+--------------------------------------------------------------------------+
        | id          | 7714c1dc-ab2c-4819-a011-58ce31cfb398                                     |
        | name        | fabric                                                                   |
        | plugin_type | deployment_plugins                                                       |
        | source      | https://github.com/cloudify-cosmo/cloudify-fabric-plugin/archive/1.2.zip |
        +-------------+--------------------------------------------------------------------------+


    $ walle-manage approved-plugins list --db-uri sqlite:////tmp/walle.db


        +--------+--------------------------------------------------------------------------+--------------------+
        | Name   | Source                                                                   | Plugin Type        |
        +--------+--------------------------------------------------------------------------+--------------------+
        | fabric | https://github.com/cloudify-cosmo/cloudify-fabric-plugin/archive/1.2.zip | deployment_plugins |
        +--------+--------------------------------------------------------------------------+--------------------+


    $ walle-manage approved-plugins delete --name --db-uri sqlite:////tmp/walle.db


=======
Testing
=======

To run code style checks please do::
.. code-block:: bash


    $ tox -e pep8 -c walle-api-server/tox.ini

    $ tox -e unittests -c walle-api-server/tox.ini

    $ tox -e integration -c walle-api-server/tox.ini

    $ tox -e validate-blueprints -c walle-api-server/tox.ini

    $ tox -e cfy-local-nodecellar -c walle-api-server/tox.ini

    $ tox -e travis-cfy-local-nodecellar-with-fabric -c walle-api-server/tox.ini

    $ tox -e travis-cfy-local-postgresql-with-fabric -c walle-api-server/tox.ini


============================
Post-Deployment verification
============================

To run post-deployment verification please do::
.. code-block:: bash


    $ export WALLE_URL=http://{walle_ip}:{walle_port}
    $ tox -e post-deployment -c walle-api-server/tox.ini


=======================================
Run integration test in real-mode
=======================================

In order to run real-mode integration tests you must add
specific flag inside commit message  body:
         RunIntegrationTests: True
Otherwise, pull request will be tested with fake-mode integration tests
(including fake vCloud and Cloudify manager).

Copy 'real-mode-tests-conf.yaml.template' to 'real-mode-tests-conf.yaml' and fill it
with correct values.

To run integration tests please do::
.. code-block:: bash

    $ export WALLE_INT_TESTS_CONF=/full/path/to/real-mode-tests-conf.yaml
    $ tox -e integration -c walle-api-server/tox.ini


