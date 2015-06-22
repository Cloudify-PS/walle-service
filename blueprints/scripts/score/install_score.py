from os import path

from cloudify import ctx
import fabric

SOURCE_HOME = path.expanduser('~')
UBUNTU_HOME = '/home/ubuntu'
SSH_DIR = '/.ssh/'
ID_RSA = 'id_rsa'


def _run(command):
    ctx.logger.info(command)
    out = fabric.api.run(command)
    ctx.logger.info(out)


def _upload_user_github_key(source_path, destination_path):
    out = fabric.api.put(source_path, destination_path)
    ctx.logger.info(out)


def install(config):
    ctx.logger.info("Config: " + str(config))
    script = []
    score_package_url = config.get('score_package_url', None)
    user_github_key = config.get('user_github_key', None)
    if score_package_url:
        script.append("""
wget -c %s -O score-service-master.tar.gz 2>&1 | tee wget_log.txt
mkdir score-service
tar -xvf score-service-master.tar.gz --strip 1 -C score-service
cd score-service/
git init
cd score-api-server/
        """ % score_package_url)
    elif user_github_key:
        _upload_user_github_key(SOURCE_HOME + SSH_DIR + user_github_key,
                                UBUNTU_HOME + SSH_DIR)
        if user_github_key != ID_RSA:
            script.append("""
mv %s %s
            """ % (UBUNTU_HOME + SSH_DIR + user_github_key,
                   UBUNTU_HOME + SSH_DIR + ID_RSA))
        script.append("""
ssh-keyscan -H github.com >> ~/.ssh/known_hosts
chmod 400 ~/.ssh/id_rsa
eval `ssh-agent`
ssh-add ~/.ssh/id_rsa
git clone git@github.com:vcloudair/score-service.git
cd score-service/score-api-server/
        """)
    script.append("""
sudo pip install -r requirements.txt && sudo python setup.py install
    """)
    _run("\n".join(script))
