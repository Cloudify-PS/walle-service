import requests
import json

# score-manage keystore-urls add --keystore-url http://192.168.0.10:5000/v2.0
# score-manage keystore-url-limits create --keystore-url http://192.168.0.10:5000/v2.0 --cloudify-host 172.25.1.15 --cloudify-port 80 --deployment-limits 100

payload = {
    "user": "admin",
    "password": "cloudify1234",
    "auth_url": "http://192.168.0.10:5000/v2.0",
    "tenant_name": "admin"
}
r = requests.post('http://127.0.0.1:5000/login_openstack', data=json.dumps(payload))
print r.content

headers = {}
headers["x-openstack-authorization"] =  json.loads(r.content) ['x-openstack-authorization']
headers["x-openstack-keystore-url"] = "http://192.168.0.10:5000/v2.0"

r = requests.get('http://127.0.0.1:5000/status', headers=headers)

print r.content

r = requests.get('http://127.0.0.1:5000/blueprints', headers=headers)

print r.content

r = requests.get('http://127.0.0.1:5000/deployments', headers=headers)

print r.content
