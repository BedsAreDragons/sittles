from flask import Flask, render_template
import requests
from datetime import datetime, timedelta

app = Flask(__name__)



@app.route('/')
def index():
    weather_data = get_weather_data()
    metar = parse_weather_data(weather_data)  # Change weather_info to weather_data
    return render_template('index.html', metar="METAR GB-0199 AUTO")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
