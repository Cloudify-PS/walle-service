#!/bin/bash

set -e
set -o xtrace

export LC_ALL=C

if [ "$SKIP_CONFIGURATION" = "False" ]; then

    echo -e "
    ALTER USER ${DB_USER} WITH PASSWORD '${DB_PASS}';
    CREATE DATABASE ${DB_USER};
    GRANT ALL ON DATABASE ${DB_NAME} TO ${DB_USER};
    " >> /tmp/psql_configure.txt

    sudo -u postgres createuser -D -S -R ${DB_USER}

    sudo -u postgres psql -c -a -f /tmp/psql_configure.txt

    sudo sed -i "s/^\(listen_addresses .*\)/# Commented out by Name `date`  \1/" -i /etc/postgresql/9.3/main/postgresql.conf
    echo "listen_addresses = '${DB_IP}'" | sudo tee -a /etc/postgresql/9.3/main/postgresql.conf

    sudo cp /etc/postgresql/9.3/main/pg_hba.conf pg_hba.conf
    sudo chmod 777 pg_hba.conf
    echo "host ${DB_NAME} ${DB_USER} ${DB_IP}/24 md5" >> pg_hba.conf
    echo "host ${DB_NAME} ${DB_USER} ${SCORE_IP}/24 md5" >> pg_hba.conf

    sudo mv pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
    sudo chmod 640 /etc/postgresql/9.3/main/pg_hba.conf
    sudo chown postgres:postgres /etc/postgresql/9.3/main/pg_hba.conf
    sudo /etc/init.d/postgresql restart

else
    echo "Skipping configuration, using existing PostgreSQL."
fi
