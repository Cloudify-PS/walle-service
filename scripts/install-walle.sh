#!/bin/sh
git clone https://github.com/Cloudify-PS/walle-service
cd walle-service/walle-api-server
pip install -r requirements.txt
pip install .
