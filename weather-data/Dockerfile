FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5001

# Umgebungsvariablen 
ENV DB_USER admin
ENV DB_PASSWORD my-weather-app-db
ENV DB_HOST my-weather-app-db.cnla9t80uygd.us-east-1.rds.amazonaws.com
ENV DB_NAME weatherdb

CMD ["python", "weather_data.py"]
