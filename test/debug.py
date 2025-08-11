import json
import requests

url = "http://localhost:8000"
resp = requests.get(url=url)
print(resp)

resp = requests.post(url=url+"/create_url", json={'url': 'https://www.google.com/'}) 
print(resp.json())
print("")