# This Dockerfile will be used as test environment box for running `CFY local` blueprint testing

FROM ubuntu:trusty

ADD . /score-service

RUN apt-get update

RUN apt-get install -qy python-dbus wget \
 python-setuptools git python-dateutil python-docutils python-feedparser \
 python-gdata python-jinja2 python-ldap python-libxslt1 python-lxml \
 python-mako python-mock python-openid python-psycopg2 python-psutil \
 python-pybabel python-pychart python-pydot python-pyparsing python-reportlab \
 python-simplejson python-tz python-unittest2 python-vatnumber python-vobject \
 python-webdav python-werkzeug python-xlwt python-yaml python-zsi \
 python-dev libxml2-dev libxslt1-dev libcr-dev zlib1g-dev python-virtualenv

# fix for ubuntu 14.04
RUN easy_install pip

RUN virtualenv /venv

RUN . /venv/bin/activate; pip install -r /score-service/score-api-server/cfy-requirements.txt
