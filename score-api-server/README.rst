====================
vCloud Score service
====================

==========
Deployment
==========

.. code-block:: bash

    $ git clone git@github.com:vchs/score-service.git
    $ cd score_api_server/
    $ virtualenv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements
    $ python setup.py install


=====
Usage
=====

Once you will accomplish deployment guide your environment will have next CLI tool::

    score-server

Usage examples::
.. code-block:: bash

    $ score-server -h

    usage: score-server [-h] [--config-dir DIR] [--version] [--config-file PATH]

    optional arguments:
      -h, --help          show this help message and exit
      --config-dir DIR    Path to a config directory to pull *.conf files from.
                          This file set is sorted, so as to provide a predictable
                          parse order if individual options are over-ridden. The
                          set is parsed after the file(s) specified via previous
                          --config-file, arguments hence over-ridden options in
                          the directory take precedence.
      --version           show program's version number and exit
      --config-file PATH  Path to a config file to use. Multiple config files can
                          be specified, with values in later files taking
                          precedence. The default files used are: None.


=============
Configuration
=============

Once you would like to change default Score API server host/port and Cloudify manager
host/port to connect to you will need to create a configuration file for score-server.
Configuration file format might have next look::

    [server]
    host = localhost
    port = 5000

    [cloudify]
    host = localhost
    port = 8000

As you can see, configuration file contains two sections::

    [server]
    [cloudify]

both this sections are responsible for Score API server configuration and Cloudifys' manager connection.

=======
Testing
=======

To run code style checks please do::
.. code-block:: bash

    $ tox -e pep8
