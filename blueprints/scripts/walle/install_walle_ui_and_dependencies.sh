#!/usr/bin/env bash
set -e
set -o xtrace

cd $HOME

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

ctx logger info "Walle URL: http://${WALLE_IP}:80"

curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
sudo apt-get update 2>&1
sudo apt-get install -qy python-software-properties python g++ make nodejs git
sudo npm install -g grunt-cli bower
sudo chown ubuntu:ubuntu $HOME -R

rm -rf walle-cloudify-ui
git clone https://github.com/Cloudify-PS/walle-cloudify-ui.git
