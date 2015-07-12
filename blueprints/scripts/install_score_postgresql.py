# Copyright (c) 2015 VMware. All rights reserved

import fabric
from cloudify import ctx


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def install(config):
    ctx.logger.info("Config: " + str(config))
    script = []
    db_user = config.get('db_user', None)
    db_name = config.get('db_name', None)
    db_pass = config.get('db_pass', None)
    script.append('sudo -u postgres createuser -D -S -R  %s' % db_user)
    script.append("""
sudo -u postgres psql -c "ALTER USER %s WITH PASSWORD '%s';"
    """ % (db_user, db_pass))
    script.append("""
sudo -u postgres psql -c "CREATE DATABASE %s;"
    """ % db_name)
    script.append("""
sudo -u postgres psql -c "GRANT ALL ON DATABASE %s TO %s;"
    """ % (db_name, db_user))
    script.append("""
sudo sed "s/#listen_addresses = 'localhost'/listen_addresses = '""" +
                  config.get('ip', "*") +
                  """'/g" -i /etc/postgresql/9.3/main/postgresql.conf
                  sudo cp /etc/postgresql/9.3/main/pg_hba.conf pg_hba.conf
                  sudo chmod 777 pg_hba.conf
                  echo "host %s %s """ % (db_name, db_user) +
                  config.get('ip_postgres', "127.0.0.1") +
                  """/24 md5" >> pg_hba.conf
                  echo "host %s %s """ % (db_name, db_user) +
                  config.get('ip_score', "127.0.0.1") +
                  """/24 md5" >> pg_hba.conf
    """)
    script.append("""
sudo mv pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
sudo chmod 640 /etc/postgresql/9.3/main/pg_hba.conf
sudo chown postgres:postgres /etc/postgresql/9.3/main/pg_hba.conf
sudo /etc/init.d/postgresql restart
    """)
    _run("\n".join(script))
