from flask import Flask, render_template
import os
import requests

app = Flask(__name__)

def get_metar():
    url = "https://api.checkwx.com/station/EGBB"
    headers = {"X-API-Key": "d67885927a1247dbaf838b7065"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)  # Add this line to inspect the structure of the response
        return data
    else:
        return "Failed to fetch METAR data"




@app.route('/')
def index():
    metar = get_metar()
    print(metar)
    return render_template('index.html', metar=metar)

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("WEB_PORT", 5000)))
