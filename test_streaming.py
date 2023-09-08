import json
import requests
# Define the URL
url = 'http://127.0.0.1:8080/summarize/'

# Define the headers
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

# Define the data as a dictionary
data = {
    "id_": "ef932ee231o562e",
    "message": "what is metamorphisis about?"
}

# Convert the data dictionary to JSON format
json_data = json.dumps(data)

# Send the POST request
response = requests.post(url, headers=headers, data=json_data)


for chunk in response.iter_lines():
    if chunk:
        print(chunk.decode("utf-8"))