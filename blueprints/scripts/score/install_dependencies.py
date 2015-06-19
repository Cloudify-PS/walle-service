from cloudify import ctx
import fabric


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def install(config):
    ctx.logger.info("Config: " + str(config))
    script = []
    script.append("""
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev libffi-dev libxml2-dev
sudo apt-get install -y libxslt-dev python-dev python-pip git
sudo apt-get install gunicorn -q -y 2>&1
sudo apt-get install nginx -q -y 2>&1
    """)
    _run("\n".join(script))
