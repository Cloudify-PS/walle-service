====================
vCloud Score service
====================

==========
Deployment
==========

.. code-block:: bash

    $ git clone http://github.com/vcloudair/score-service.git
    $ cd score-service/score-api-server/
    $ virtualenv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
    $ python setup.py install


=====
Usage
=====

Before run call db update/creation by:
    $   export SCORE_DB="sqlite:////tmp/score-service.db"
        score-manage db upgrade

Also SCORE_DB can be postgresql://score:secret-password@localhost/score

And only first time please import sql from initial.sql to db.

Once you will accomplish deployment guide your environment will have next CLI tool::

    score-server

Usage examples::
.. code-block:: bash

    $ export SCORE_HOST="0.0.0.0"; \
      export SCORE_PORT="5000"; \
      export SCORE_WORKERS="4";\
      export CFY_MANAGER_HOST="127.0.0.1"; \
      export CFY_MANAGER_PORT="80"; \
      export SCORE_DB="sqlite:////tmp/score-service.db"; \
      score-server

      * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

====================
Gunicorn integration
====================

To run score-server app under gunicorn please use this command
.. code-block::bash

    $ pip install gunicorn
    $ gunicorn -h

        usage: gunicorn [OPTIONS] [APP_MODULE]


Usage examples::
.. code-block:: bash

    $ export SCORE_HOST="0.0.0.0"; \
      export SCORE_PORT="5000"; \
      export SCORE_WORKERS="4"
      export CFY_MANAGER_HOST="127.0.0.1"; \
      export CFY_MANAGER_PORT="80"; \
      export SCORE_DB="sqlite:////tmp/score-service.db"; \
      gunicorn -w ${SCORE_WORKERS} -b ${SCORE_HOST}:${SCORE_PORT} score_api_server.cli.app:main

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

Once you would like to change default Score API server host/port and Cloudify manager
host/port to connect to you will need to create a configuration file for score-server.
Configuration environment variables might have next look::
.. code-block:: bash

    $ export SCORE_HOST="0.0.0.0"
    $ export SCORE_PORT="5000"
    $ export SCORE_WORKERS="4"

    $ export CFY_MANAGER_HOST="127.0.0.1"
    $ export CFY_MANAGER_PORT="80"
    # export SCORE_DB="sqlite:////tmp/score-service.db"


==============
Administration
==============

New CLI tool 'score-manage' does allow to add new Org-ID during Score service runtime.
Here's an example of you can use this tool::
.. code-block:: bash

    $ score-manage org-ids

        usage: Performs action related to Org-IDs

        Performs action related to Org-IDs

        positional arguments:
          {add,list,delete}
            add              Adds Org-ID.
            list             Lists Org-IDs.
            delete           Deletes Org-ID.

        optional arguments:
          -?, --help         show this help message and exit



    $ score-manager org-ids add --org-id 4174a0c7-cd86-4dc8-a784-2cb5b852e823 sqlite:////tmp/score.db --db-uri sqlite:////tmp/score.db

        +----------+--------------------------------------+
        | Property | Value                                |
        +----------+--------------------------------------+
        | id       | 32ba94e2-b1bc-4b21-90e6-ca1e98c7335d |
        | org_id   | 4174a0c7-cd86-4dc8-a784-2cb5b852e823 |
        +----------+--------------------------------------+



    $ score-manage org-ids list --db-uri sqlite:////tmp/score.db

        +--------------------------------------+--------------------------------------+
        | ID                                   | Org ID                               |
        +--------------------------------------+--------------------------------------+
        | 32ba94e2-b1bc-4b21-90e6-ca1e98c7335d | 4174a0c7-cd86-4dc8-a784-2cb5b852e823 |
        | 79e12239-08de-40ab-a56b-090a76c9a351 | 66d1c056-4bc2-4ac4-88f6-7b2e83244742 |
        | dfe663d8-8ee1-44e1-97dc-8c2a5ba67142 | 2b876939-f76d-4436-80fa-3a43a5f3f83f |
        +--------------------------------------+--------------------------------------+



    $ score-manage org-ids delete --org-id 4174a0c7-cd86-4dc8-a784-2cb5b852e823 --db-uri sqlite:////tmp/score.db

        OK


    $ score-manage org-ids list

        +--------------------------------------+--------------------------------------+
        | ID                                   | Org ID                               |
        +--------------------------------------+--------------------------------------+
        | 79e12239-08de-40ab-a56b-090a76c9a351 | 66d1c056-4bc2-4ac4-88f6-7b2e83244742 |
        | dfe663d8-8ee1-44e1-97dc-8c2a5ba67142 | 2b876939-f76d-4436-80fa-3a43a5f3f83f |
        +--------------------------------------+--------------------------------------+


=======
Testing
=======

To run code style checks please do::
.. code-block:: bash

    $ tox -e pep8
    $ tox -e unittests
