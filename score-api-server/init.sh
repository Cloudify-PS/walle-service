score-manage db upgrade
score-manage keystore-urls add --keystore-url http://192.168.0.10:5000/v2.0
score-manage keystore-url-limits add --keystore-url http://192.168.0.10:5000/v2.0 --cloudify-host 172.25.1.21 --cloudify-port 80 --deployment-limits 100
score-manage approved-plugins add --from-file ../approved_plugins/approved_plugins_description.yaml

