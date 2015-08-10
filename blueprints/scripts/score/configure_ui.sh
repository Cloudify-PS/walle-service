#!/bin/bash

set -e
set -o xtrace

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive

echo "Installing Score UI"

mkdir score-ui-src
tar -xvf score-ui-src.tar.gz -C score-ui-src

rm -fr www/*

mv score-ui-src ~/www/score

sudo service nginx restart
