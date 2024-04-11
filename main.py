from flask import Flask, render_template
import requests
from datetime import datetime, timedelta

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

def parse_weather_data(data):
    if data is None or 'hourly' not in data:
        return None

    current_time_london = datetime.utcnow() + timedelta(hours=1)
    current_hour = current_time_london.hour

    # Extracting relevant weather information
    hourly_data = data['hourly']
    if not hourly_data:
        return None

    # Assuming we're interested in the first hourly forecast
    if current_hour >= len(hourly_data):
        return None

    forecast_data = hourly_data[current_hour]
    
    temperature = forecast_data.get('temperature_2m')
    dew_point = forecast_data.get('dew_point_2m')
    wind_speed = forecast_data.get('wind_speed_10m')
    wind_direction = forecast_data.get('wind_direction_10m')
    wind_gusts = forecast_data.get('wind_gusts_10m')
    pressure = forecast_data.get('surface_pressure')

    if any(val is None for val in [temperature, dew_point, wind_speed, wind_direction, wind_gusts, pressure]):
        return None

    # Format time in Zulu
    current_time_zulu = current_time_london.strftime("%d%H%MZ")

    # Format wind direction and speed
    wind_direction_str = "{:03d}".format(wind_direction)
    wind_speed_str = "{:02d}".format(round(wind_speed))
    wind_gusts_str = "{:02d}".format(round(wind_gusts))

    realtemp = round(temperature)
    realdew = round(dew_point)

    # Format METAR-like string
    metar = f"METAR GB-0199 AUTO {current_time_zulu} {wind_direction_str}{wind_speed_str}KT {realtemp}/{realdew} Q{int(pressure)}"

    return metar


@app.route('/')
def index():
    weather_data = get_weather_data()
    metar = parse_weather_data(weather_info)
    return render_template('index.html', metar=metar)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
