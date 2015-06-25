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
        python score_api_server/cli/manage.py db upgrade

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

=======
Testing
=======

To run code style checks please do::
.. code-block:: bash

    $ tox -e pep8
    $ tox -e unittests
