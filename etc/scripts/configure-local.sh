#!/bin/bash

PRJ=~/vca/walle-service/walle-api-server

cd $PRJ
virtualenv $PRJ/.venv
source $PRJ/.venv/bin/activate

pip install gunicorn

pip install --edit ~/vca/pyvcloud

pip install -r $PRJ/requirements.txt
pip install -r $PRJ/test-requirements.txt

pip install --edit $PRJ
