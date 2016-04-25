#!/bin/bash
set -e
set -o xtrace

cd ~

export DEBIAN_FRONTEND=noninteractive
if [ x"$SKIP_INSTALLATION" != x"true" ]; then

    echo "Installing postgresql."

    echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -c | awk '{print $2}'`-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update
    sudo apt-get -qy install postgresql-9.3 pgadmin3

else
    echo "Skipping installation, using existing PostgreSQL."
fi
