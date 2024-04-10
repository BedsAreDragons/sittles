from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.6815,
        "longitude": -1.8255,
        "hourly": "temperature_2m,dew_point_2m,surface_pressure,cloud_cover,visibility,wind_speed_10m,wind_direction_10m,wind_gusts_10m",
        "wind_speed_unit": "kn",
        "timezone": "Europe/London",
        "forecast_days": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch weather data: {e}")
        return None

@app.route('/')
def index():
    weather_data = get_weather_data()
    metar = parse_weather_data(weather_data)
    return render_template('index.html', metar=metar)

def parse_weather_data(data):
    if data is None:
        return None

    # Extracting relevant weather information
    hourly_data = data['hourly'][0]  # Assuming we're interested in the first hourly forecast
    wind_speed = hourly_data['wind_speed_10m']
    wind_direction = hourly_data['wind_direction_10m']

    # Constructing METAR-like information
    metar = f"METAR GB-0199 (INFO) {wind_direction:03d}{wind_speed:02d}KT"

    return metar

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

