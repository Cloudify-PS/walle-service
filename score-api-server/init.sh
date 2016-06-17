score-manage db upgrade
score-manage service-urls add --service-url http://192.168.0.10:5000/v2.0 --tenant=admin
score-manage service-url-limits add --service-url http://192.168.0.10:5000/v2.0 --cloudify-host 172.25.1.43 --cloudify-port 80 --deployment-limits 100 --tenant=admin
score-manage approved-plugins add --from-file ../approved_plugins/approved_plugins_description.yaml
score-manage users add --user root --password root

#score-manage-cli login root root http://127.0.0.1:5000
#score-manage-cli service_urls add --service-url service_url_test --tenant tenant_test
#score-manage-cli service_url_limits add --service-url service_url_test --tenant tenant_test --cloudify-host 172.25.1.43 --cloudify-port 80 --deployment-limits 100
