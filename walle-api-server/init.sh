walle-manage db upgrade
walle-manage endpoints add --endpoint-url http://192.168.0.10:5000/v2.0 --type openstack
walle-manage tenants add --endpoint-url http://192.168.0.10:5000/v2.0 --type openstack --cloudify-host 172.25.1.75 --cloudify-port 80 --tenant admin
walle-manage limits add --endpoint-url http://192.168.0.10:5000/v2.0 --type openstack --tenant admin --hard 100 --soft 90 --limit-type deployments
walle-manage rights add --name tenants
walle-manage tenantrights add --endpoint-url http://192.168.0.10:5000/v2.0 --type openstack --tenant admin --right tenants
walle-manage approved-plugins add --from-file ../approved_plugins/approved_plugins_description.yaml
walle-manage users add --user root --password root

#walle-manage-cli login root root http://127.0.0.1:5000
#walle-manage-cli endpoint_urls add --endpoint-url service_url_test --type tenant_test
#walle-manage-cli tenants add --endpoint-url service_url_test --type tenant_test --cloudify-host 172.25.1.75 --cloudify-port 80 --tenant-name admin
#walle-manage-cli limits add --endpoint-url service_url_test --type tenant_test --tenant admin --hard 100 --soft 90 --limit-type deployments
