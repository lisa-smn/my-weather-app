FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip install gunicorn

COPY . .

EXPOSE 8080

ENV API_KEY bb97533805fced5bb8e6af83e94dbee8
ENV S3_BUCKET_NAME weatherforecast
ENV FLASK_ENV production
ENV DB_USER admin
ENV DB_PASSWORD your-password
ENV DB_HOST my-weather-app-db.cnla9t80uygd.us-east-1.rds.amazonaws.com
ENV DB_NAME weatherdb

# Run app with Gunicorn when the container launches
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
