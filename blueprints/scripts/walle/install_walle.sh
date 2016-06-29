#!/bin/bash

set -e
set -o xtrace

cd ~

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

rm -f walle-service.tar.gz
curl -o walle-service.tar.gz ${WALLE_PACKAGE_URL}  2>&1
mkdir -p walle-service
tar -xvf walle-service.tar.gz -C walle-service 2>&1
cd walle-service/
git init
cd walle-api-server/
sudo python setup.py install 2>&1
