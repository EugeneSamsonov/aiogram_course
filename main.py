import requests

URL = requests.get("http://numbersapi.com/43")
print(URL.text)
