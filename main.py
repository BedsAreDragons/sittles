from flask import Flask, render_template
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

metars()

def metars():
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.706958&longitude=-1.75018&hourly=temperature_2m,dew_point_2m,rain,snowfall,pressure_msl,cloud_cover,visibility,wind_speed_180m,wind_direction_180m,wind_gusts_10m&wind_speed_unit=kn&timezone=Europe%2FLondon&forecast_days=1"

# Get current time in London
    current_time_london = datetime.utcnow() + timedelta(hours=1)
    current_hour = current_time_london.hour

# Make request
    response = requests.get(url)
    data = response.json()

# Calculate index based on live hour
    index = current_hour

# Extract information
    temperature = data["hourly"]["temperature_2m"][index]
    dew_point = data["hourly"]["dew_point_2m"][index]
    rain = data["hourly"]["rain"][index]
    snowfall = data["hourly"]["snowfall"][index]
    pressure = data["hourly"]["pressure_msl"][index]
    cloud_cover = data["hourly"]["cloud_cover"][index]
    visibility = data["hourly"]["visibility"][index]
    wind_speed = data["hourly"]["wind_speed_180m"][index]
    wind_direction = data["hourly"]["wind_direction_180m"][index]
    wind_gusts = data["hourly"]["wind_gusts_10m"][index]

# Format time in Zulu
    current_time_zulu = current_time_london.strftime("%d%H%MZ")

# Format wind direction and speed
    wind_direction_str = "{:03d}".format(wind_direction)
    wind_speed_str = "{:02d}".format(round(wind_speed))
    wind_gusts_str = "{:02d}".format(round(wind_gusts))

# Format visibility in meters
    visibility_meters = "{:04d}".format(round(visibility))

    realtemp = round(temperature)
    realdew = round(dew_point)

# Format METAR-like string
    metar = f"METAR GB-0199 AUTO {current_time_zulu} {wind_direction_str}{wind_speed_str}KT {realtemp}/{realdew} Q{int(pressure)}"
    print("METAR:", metar)


@app.route('/')
def index():
    metar = f"METAR GB-0199 AUTO {current_time_zulu} {wind_direction_str}{wind_speed_str}KT {realtemp}/{realdew} Q{int(pressure)}"
    return render_template('index.html', metar=metar)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
