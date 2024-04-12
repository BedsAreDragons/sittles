from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    metar = "METAR GB-0199 AUTO {}Z".format(now) # Change weather_info to weather_data
    return render_template('index.html', metar=metar)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
