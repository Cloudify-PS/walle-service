# Copyright (c) 2015 VMware. All rights reserved

import fabric
from cloudify import ctx


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def _generate_service(server_host, db_url):
    return [
        "description 'score service'",
        "# used to be: start on startup",
        "# until we found some mounts were not ready yet while booting:",
        "start on started mountall",
        "stop on shutdown",
        "# Automatically Respawn:",
        "respawn",
        "respawn limit 99 5",
        "script",
        "    export SCORE_HOST=%s" % server_host,
        "    export SCORE_PORT=8001",
        "    export SCORE_WORKERS=4",
        "    export SCORE_DB=%s" % db_url,
        "    exec /usr/bin/gunicorn -w 4 -b localhost:8001 " +
        "score_api_server.cli.app:app 2>&1 > /tmp/log",

        "end script"
    ]


def configure(config):
    ctx.logger.info("Config: " + str(config))
    script = []
    server_host = config.get("score_ip", "0.0.0.0")
    db_user = config.get('db_user', None)
    db_name = config.get('db_name', None)
    db_pass = config.get('db_pass', None)
    db_ip = config.get("db_ip", "localhost")

    db_url = ("postgresql://%s:%s@" % (db_user, db_pass) +
              db_ip + "/%s" % db_name)
    # create service config
    service = _generate_service(server_host, db_url)
    ctx.logger.info(service)
    script.append("rm -f /home/ubuntu/score_api_server.conf")
    for service_str in service:
        script.append('echo "' + service_str +
                      '" >> /home/ubuntu/score_api_server.conf')
    # create db
    script.append('pwd')  # Needs to be known which the user executes commands
    script.append('mkdir -p /home/ubuntu/score_logs')
    script.append(
        'echo export SCORE_LOGGING_FILE=/home/ubuntu/score_logs/score-api.log '
        '>> ~/.bashrc')
    script.append('echo export SCORE_DB=%s >> ~/.bashrc' % db_url)
    script.append('echo export SCORE_LOGGING_LEVEL=INFO >> ~/.bashrc')
    script.append('sudo -u ubuntu source /home/ubuntu/.bashrc')
    # create init file
    script.append("""
sudo cp /home/ubuntu/score_api_server.conf /etc/init/score_api_server.conf
sudo chown root:root /etc/init/score_api_server.conf
# run service
sudo initctl start score_api_server
    """)
    # configure nginx service
    script.append("""
sudo rm /etc/nginx/sites-enabled/*
sudo cp /home/ubuntu/score-service/etc/nginx/vca_io /etc/nginx/sites-enabled
sudo cp /home/ubuntu/score-service/etc/keys/* /etc/nginx/
sudo service nginx restart
    """)
    _run("\n".join(script))
