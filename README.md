# My Weather App

My Weather App is a web application that displays current weather information for a given city. The weather data is fetched from the OpenWeatherMap API and stored in an AWS S3 bucket.

## Features

- Retrieve weather information for a specified city
- Save weather data to AWS S3
- Display weather information on a web page

## Prerequisites

- Python 3.x
- Flask
- boto3
- requests
- OpenWeatherMap API Key
- AWS account with S3 bucket

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/lisa-smn/my-weather-app.git
    cd my-weather-app
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set environment variables for AWS credentials:

    ```bash
    export AWS_ACCESS_KEY_ID=your_access_key
    export AWS_SECRET_ACCESS_KEY=your_secret_key
    export AWS_DEFAULT_REGION=your_region
    ```

4. Create a file `config.py` and add your OpenWeatherMap API Key:

    ```python
    API_KEY = 'your_openweathermap_api_key'
    ```

## Usage

1. Start the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and go to `http://localhost:5000`.

3. Enter the name of a city and click "Get Weather" to display the weather information.

## Docker

1. Pull the Docker image from Docker Hub:

    ```bash
    docker pull lisasmn/my-weather-app:latest
    ```

2. Run the Docker container:

    ```bash
    docker run -d -p 8080:8080 lisasmn/my-weather-app:latest
    ```

## AWS Deployment

1. Create an S3 bucket named `weatherforecast`.

2. Upload your static files (HTML, CSS, JS) to the S3 bucket and make them publicly accessible.

3. Use the S3 bucket URL to access the website.


## License

This project is licensed under the MIT License. See the LICENSE file for details.
