import requests
import json

access_key = 'fe66583bfe5185048c66571293e0d358'

url = 'https://globalmart-api.onrender.com/mentorskool/v1/sales'

header = {'access_token': access_key}

response = requests.get(url, headers=header)

data = json.loads(response.text)
print(data)