#!/bin/bash
set -e
set -o xtrace

cd $HOME

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

ctx logger info "Installing Walle UI"

rm -fr www/*

cp -rv walle-cloudify-ui $HOME/www/walle

cd $HOME/www/walle

ctx logger info "running npm install"
npm install || ctx logger info "npm failed"

ctx logger info "running bower install"
bower install --allow-root || ctx logger info "bower failed"

ctx logger info "install optional dependencies"
npm install phantomjs || ctx logger info "phantomjs failed"

ctx logger info "rebuild node-sass"
npm rebuild node-sass || ctx logger info "node-sass failed"

cd $HOME

sudo service nginx restart

mkdir -p /home/ubuntu/www/walle/conf/dev/

echo -e  "
var exports = module.exports = {
    cloudifyManagerEndpoint: 'http://${WALLE_INTERNAL_IP_ADDRESS}:8001/',
    port: '80'
}
" > /home/ubuntu/www/walle/conf/dev/meConf.js

# Grunt
echo -e "
description 'grunt walle service'
# used to be: start on startup
# until we found some mounts were not ready yet while booting
start on started mountall
stop on shutdown
# Automatically Respawn:
respawn
respawn limit 99 5
setuid ubuntu
setgid ubuntu
script
    exec grunt --gruntfile /home/ubuntu/www/walle/Gruntfile.js server --force 2>&1
end script
" >> $HOME/walle_grunt.conf

sudo cp $HOME/walle_grunt.conf /etc/init/walle_grunt.conf

sudo chown root:root /etc/init/walle_grunt.conf
sudo initctl start walle_grunt

# nodejs
echo -e "
description 'nodejs walle service'
# used to be: start on startup
# until we found some mounts were not ready yet while booting
start on started mountall
stop on shutdown
# Automatically Respawn:
respawn
respawn limit 99 5
setuid ubuntu
setgid ubuntu
script
    exec /usr/bin/nodejs /home/ubuntu/www/walle/server.js 2>&1
end script
" >> $HOME/walle_nodejs.conf

sudo cp $HOME/walle_nodejs.conf /etc/init/walle_nodejs.conf

sudo chown root:root /etc/init/walle_nodejs.conf
sudo initctl start walle_nodejs
