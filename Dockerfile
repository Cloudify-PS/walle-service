# This Dockerfile will be used as test environment box for running `CFY LOCAL` blueprint testing

FROM ubuntu:trusty

ADD . /walle-service

RUN cd /; rm -fr walle-service/.venv walle-service/.git walle-service/walle-api-server/.tox

RUN apt-get update

RUN apt-get install -qy python-dbus wget \
 python-setuptools git python-dateutil python-docutils python-feedparser \
 python-gdata python-jinja2 python-ldap python-libxslt1 python-lxml \
 python-mako python-mock python-openid python-psycopg2 python-psutil \
 python-pybabel python-pychart python-pydot python-pyparsing python-reportlab \
 python-simplejson python-tz python-unittest2 python-vatnumber python-vobject \
 python-webdav python-werkzeug python-xlwt python-yaml python-zsi \
 python-dev libxml2-dev libxslt1-dev libcr-dev zlib1g-dev python-virtualenv openssh-server

# fix for ubuntu 14.04
RUN easy_install pip

RUN virtualenv /venv

RUN . /venv/bin/activate; pip install -r /walle-service/walle-api-server/cfy-requirements.txt

RUN cd /;tar -czf walle-service.tar.gz walle-service

RUN cd /; tar -czf walle-nginx-configuration.tar.gz walle-service/etc walle-service/www

RUN ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa

RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

RUN chmod 755 /root/.ssh/authorized_keys

RUN echo -e "StrictHostKeyChecking no\n" >> /root/.ssh/config

RUN mkdir /var/run/sshd

RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN service ssh restart

# Setting up inputs file for local locablueprint execution including Walle blueprint

RUN cd /; touch inputs-cfy-local.yaml

RUN cd /; echo -e "servers_user: root\n" >> inputs-cfy-local.yaml

RUN cd /; echo -e "private_key_path: /root/.ssh/id_rsa\n" >> inputs-cfy-local.yaml

RUN cd /; echo -e "servers_user: root\n" >> inputs-cfy-local.yaml

RUN cd /; echo -e "host_string: localhost\n" >> inputs-cfy-local.yaml
