from flask import Flask, request, jsonify
import mysql.connector
import os
import requests

app = Flask(__name__)

# Datenbankkonfiguration aus Umgebungsvariablen laden
db_config = {
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'my-weatther-app-db'),
    'host': os.getenv('DB_HOST', 'my-weather-app-db.cnla9t80uygd.us-east-1.rds.amazonaws.com'),
    'database': os.getenv('DB_NAME', 'weatherdb')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def fetch_and_store_weather(city):
    api_key = os.getenv('API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
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
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data from API: {e}")
    except mysql.connector.Error as err:
        print(f"Error storing weather data to database: {err}")

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
    app.run(host='0.0.0.0', port=5001)
