#!/bin/bash
set -e
set -o xtrace

cd $HOME

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

echo "Installing Walle UI"

mkdir -p walle-ui-src
tar -xvf walle-ui-src.tar.gz -C walle-ui-src

rm -fr www/*

mv walle-ui-src $HOME/www/walle

sudo service nginx restart
