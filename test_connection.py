import requests
response = requests.get("http://weather-data:5001/weather")
print(response.status_code)
print(response.json())

