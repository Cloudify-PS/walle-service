#!/bin/bash

PRJ=/home/ubuntu/score-service

cd $PRJ
virtualenv $PRJ/venv
source $PRJ/venv/bin/activate

pip install gunicorn

pip install -r $PRJ/score-api-server/requirements.txt
pip install -r $PRJ/score-api-server/test-requirements.txt

cd $PRJ/score-api-server
python setup.py install
