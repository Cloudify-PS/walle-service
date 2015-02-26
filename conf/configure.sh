#!/bin/bash

#!/bin/bash

PRJ=/home/ubuntu/score-service

cd $PRJ
virtualenv $PRJ/venv
source $PRJ/venv/bin/activate

pip install gunicorn

pip install $PRJ/score-api-server

