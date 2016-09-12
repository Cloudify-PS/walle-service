#!/bin/sh
wget http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/get-cloudify.py
python get-cloudify.py --version=3.4
git clone https://github.com/kostya13/manager-blueprint-for-datacentred cloudify-manager-blueprints
