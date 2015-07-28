=================================
Run cfy local in docker container
=================================

===============
Build container
===============

In order to create a docker container you need be in project root directory
and run next commands::
.. code-block:: bash


    docker build -t cfy-local .


Once build is done you will see such output::


    Successfully built 2d6c0aa93773


=============
Run container
=============

Before that you need to log in into container::
.. code-block:: bash


    docker run -i -t 2d6c0aa93773 /bin/bash


Once you're in, for cfy-local workflows you need to::

    * start HTTP server for Score and NGINX configuration packages
    * activate virtualenv that was create during image build
    * start testing local blueprints, all blueprints are located at "/score-service",
      for Score local blueprint all necessary files are placed at root folder,
      inputs file for local bluprints is located inside root folder.


Commands::
.. code-block:: bash

    cd /; python -m SimpleHTTPServer 8000 >/dev/null 2>&1 &

    source /venv/bin/activate

    cd /; cfy local init -p score-service/blueprints/vcloud-score-blueprint-local-with-fabric.yaml -i inputs-cfy-local.yaml

