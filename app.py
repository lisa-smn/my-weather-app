import requests
import json
import boto3
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Funktion zum Abrufen der Wetterdaten
def get_weather(city):
    api_key = 'bb97533805fced5bb8e6af83e94dbee8'  
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    
    if response.status_code == 200:
        main = data['main']
        wind = data['wind']
        weather_desc = data['weather'][0]['description']
        
        weather_info = {
            'Temperature': main['temp'],
            'Humidity': main['humidity'],
            'Pressure': main['pressure'],
            'Weather Description': weather_desc,
            'Wind Speed': wind['speed'],
            'Timestamp': datetime.utcnow().isoformat()
        }
        
        # Speichern der Wetterdaten in AWS S3
        save_weather_to_s3(city, weather_info)
        
        return weather_info
    else:
        return {"Error": "City not found"}

# Funktion zum Speichern der Wetterdaten in AWS S3
def save_weather_to_s3(city, weather_info):
    s3 = boto3.client('s3')
    bucket_name = 'weatherforecast' 
    file_name = f"weather_data/{city}_{weather_info['Timestamp']}.json"
    
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(weather_info),
        ContentType='application/json'
    )

# Route für die Startseite
@app.route('/')
def index():
    return render_template('index.html')

# Route für die Wetter-API
@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    if not city:
        return jsonify({"Error": "City not provided"}), 400
    weather_info = get_weather(city)
    return jsonify(weather_info)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
