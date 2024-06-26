from flask import Flask, request, jsonify
import mysql.connector
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Datenbankkonfiguration aus Umgebungsvariablen laden
db_config = {
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'your-password'),
    'host': os.getenv('DB_HOST', 'my-weather-app-db.cnla9t80uygd.us-east-1.rds.amazonaws.com'),
    'database': os.getenv('DB_NAME', 'weatherdb')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def fetch_and_store_weather(city):
    api_key = os.getenv('API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO weather (city, temperature, description) VALUES (%s, %s, %s)',
            (data['name'], data['main']['temp'], data['weather'][0]['description'])
        )
        conn.commit()
        cursor.close()
        conn.close()

@app.route('/weather', methods=['GET'])
def get_weather():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM weather')
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/weather', methods=['POST'])
def add_weather():
    data = request.get_json()
    fetch_and_store_weather(data['city'])
    return '', 201

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_and_store_weather, trigger="interval", seconds=3600, args=['Hamburg'])  # Fetched weather data for Hamburg every hour
    scheduler.start()
    app.run(host='0.0.0.0', port=5001)
