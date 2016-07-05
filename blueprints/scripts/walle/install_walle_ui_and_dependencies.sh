#!/usr/bin/env bash
set -e
set -o xtrace

cd $HOME

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive


echo "Walle package URL: ${WALLE_UI_PACKAGE_URL}"
echo "Walle URL: http://${WALLE_IP}:80"

curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get update 2>&1

sudo apt-get -qy install nodejs make g++ git
sudo npm install -g grunt-cli bower

rm -f walle-ui-src.tar.gz
curl -o walle-ui-src.tar.gz ${WALLE_UI_PACKAGE_URL}
