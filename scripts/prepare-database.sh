#!/bin/sh
export ENDPOINT_URL="https://compute.datacentred.io:5000"
export TENANT_NAME="gigaspaces_field_engineers"
export CLOUDIFY_HOST="185.98.150.70"

walle-manage db upgrade
walle-manage endpoints add --endpoint-url $ENDPOINT_URL --type openstack
walle-manage tenants add --endpoint-url $ENDPOINT_URL --type openstack --cloudify-host $CLOUDIFY_HOST --cloudify-port 80 --tenant $TENANT_NAME
walle-manage limits add --endpoint-url $ENDPOINT_URL --type openstack --tenant $TENANT_NAME --hard 100 --soft 90 --limit-type deployments
walle-manage approved-plugins add --from-file ../approved_plugins/approved_plugins_description.yaml
walle-manage rights add --name tenants
walle-manage rights add --name plugins
walle-manage rights add --name admin
#walle-manage userrights add --username "" --password "" --endpoint-url $ENDPOINT_URL --tenant $TENANT_NAME --type "openstack" --right "admin"

