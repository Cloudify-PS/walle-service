import requests

headers = {}
headers["x-openstack-authorization"] = "something"
headers["x-openstack-keystore-url"] = "http://some.url.keystore"


r = requests.get('http://127.0.0.1:5000/status', headers=headers)

print r.content
