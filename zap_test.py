import requests

try:
    response = requests.get("http://127.0.0.1:8080/JSON/core/view/version/")
    print("ZAP Version:", response.json())
except Exception as e:
    print("Error connecting to ZAP:", e)
