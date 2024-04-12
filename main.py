from flask import Flask, render_template
import requests
from datetime import datetime, timedelta

app = Flask(__name__)






@app.route('/')
def index():
    return render_template('index.html', metar=metar)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
