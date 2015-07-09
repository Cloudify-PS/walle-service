#!/bin/bash

export LC_ALL=C
sudo apt-get update 2>&1
sudo apt-get install -y postgresql=9.1+129ubuntu1  2>&1
sudo apt-get install -y postgresql-contrib=9.1+129ubuntu1 2>&1
