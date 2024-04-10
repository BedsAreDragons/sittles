from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_metar():
    url = "https://avwx.rest/api/metar/EGBB"
    headers = {"Authorization": "Token my_secret_api_token"}
    params = {
        "format": "json"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['sanitized']  # 'sanitized' key contains the METAR information
    else:
        return "Failed to fetch METAR data"

@app.route('/')
def index():
    metar = get_metar()
    return render_template('index.html', metar=metar)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
