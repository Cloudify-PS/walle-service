#!/bin/bash

#!/bin/bash

PRJ=/home/ubuntu/score-service

cd $PRJ
source $PRJ/venv/bin/activate

pip install gunicorn

pip install score-api-server

cd $PRJ/score-api-server/score_api_server

$PRJ/venv/bin/gunicorn -w 1 -b 127.0.0.1:8001 app:app