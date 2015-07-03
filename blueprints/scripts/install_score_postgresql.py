# Copyright (c) 2015 VMware. All rights reserved

import fabric
from cloudify import ctx


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def install(config):
    ctx.logger.info("Config: " + str(config))
    _run("""
sudo -u postgres createuser -D -S -R  score
sudo -u postgres psql -c \
    "ALTER USER score WITH PASSWORD 'secret-password';"
sudo -u postgres psql -c "CREATE DATABASE score;"
sudo -u postgres psql -c "GRANT ALL ON DATABASE score TO score;"
sudo sed "s/#listen_addresses = 'localhost'/listen_addresses = '"""
         + config.get('ip', "*") + """'/g"\
  -i /etc/postgresql/9.1/main/postgresql.conf
sudo cp /etc/postgresql/9.1/main/pg_hba.conf pg_hba.conf
sudo chmod 777 pg_hba.conf
echo "host score score """ + config.get('ip', "127.0.0.1")
         + """/32 md5" >> pg_hba.conf
sudo mv pg_hba.conf /etc/postgresql/9.1/main/pg_hba.conf
sudo chmod 640 /etc/postgresql/9.1/main/pg_hba.conf
sudo chown postgres:postgres /etc/postgresql/9.1/main/pg_hba.conf
sudo /etc/init.d/postgresql restart
""")
