import json
import requests
import time 
# Define the URL
url = 'http://127.0.0.1:8000/question_answering/'

# Define the headers
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

# Define the data as a dictionary
data = {
    "message_id": "ef932ee231o562e",
    "message": "what's the name of metamorphisis the book protaganest?"
}

# Convert the data dictionary to JSON format
json_data = json.dumps(data)
try:
    response=requests.post(url, headers=headers, data=json_data, stream=True)
    content_type = response.headers.get("content-type")
    
    for chunk in response.iter_content(chunk_size=10):  # Adjust chunk_size as needed
        if chunk:
            # Process or print each chunk as it arrives
            print(chunk.decode(), end="")
        else:
            print(f"Unexpected content type: {content_type}")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
