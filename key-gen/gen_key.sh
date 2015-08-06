#!/bin/bash
echo "please use 'score' as pass phrase"
openssl genrsa -des3 -out server.key 2048
# Signing request
openssl req -new -key server.key -out server.csr -batch
# Remove the Passphrase
cp server.key server.key.org
openssl rsa -in server.key.org -out server.key
# Sign your SSL Certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
mkdir -p ../etc/keys
mv server.crt server.key ../etc/keys

# ssh keys for login
ssh-keygen -t rsa -b 4096 -C "score@getcloudify.org" -f key
