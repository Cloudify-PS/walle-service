import requests

# score-manage keystore-urls add --keystore-url http://192.168.0.10:5000/v2.0
# score-manage keystore-url-limits create --keystore-url http://192.168.0.10:5000/v2.0 --cloudify-host 172.25.1.15 --cloudify-port 80 --deployment-limits 100

headers = {}
headers["x-openstack-authorization"] = "something"
headers["x-openstack-keystore-url"] = "http://192.168.0.10:5000/v2.0"


r = requests.get('http://127.0.0.1:5000/status', headers=headers)

print r.content
