import requests

query = "How tall is the Eiffel tower?"
url = "http://localhost:8080/summarize"
params = {"message": query, 
          "id_":"mde23klllmzleke"}

response = requests.post(url, params=params, stream=True)

for chunk in response.iter_lines():
    if chunk:
        print(chunk.decode("utf-8"))