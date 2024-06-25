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

# Run app with Gunicorn when the container launches
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
