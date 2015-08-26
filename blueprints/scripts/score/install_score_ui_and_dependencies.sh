#!/usr/bin/env bash

set -e
set -o xtrace

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive


echo "Score package URL: ${SCORE_UI_PACKAGE_URL}"
echo "Score URL: http://${SCORE_IP}:80"

curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get update 2>&1

sudo apt-get -qy install nodejs make g++ git
sudo npm install -g grunt-cli bower

curl -o score-ui-src.tar.gz ${SCORE_UI_PACKAGE_URL}
