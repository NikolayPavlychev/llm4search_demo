import requests

url = 'http://0.0.0.0:8002/api/v1/igla-chat/ask/'
json_data = {"question":"Что такое IGLA X?"}
headers = {'content-type': 'application/json', 'accept': 'application/json'}

r =requests.post(url, json=json_data, headers=headers)
r.text