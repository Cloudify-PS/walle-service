#!/usr/bin/env bash
set -e
set -o xtrace

cd ~

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive


echo "Score package URL: ${WALLE_UI_PACKAGE_URL}"
echo "Score URL: http://${WALLE_IP}:80"

curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get update 2>&1

sudo apt-get -qy install nodejs make g++ git
sudo npm install -g grunt-cli bower

rm -f score-ui-src.tar.gz
curl -o score-ui-src.tar.gz ${WALLE_UI_PACKAGE_URL}
