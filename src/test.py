import requests
import json

queries = ['Time and Tide wait for None', 'Slow and Steady Wins the race']

input = {'queries':queries}
 
response = requests.post('http://0.0.0.0:8080/predictions/<NAME_OF_THE_MODEL>', data={'data':json.dumps(input)})
print(response, response.status_code, response.text, response.headers)

data = response.content

print(data)