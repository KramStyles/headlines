from flask import Flask, render_template, request
import json, requests

app = Flask(__name__)


@app.route('/')
def index():
    DEFAULTS = {
        'api_key': '7826b779b9c7e0768b8f1a46228110a3',
        'city': 'Enugu'
    }
    sta = 'aba'
    city = request.args.get('city')
    api_url = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&units=metric&appid="+DEFAULTS['api_key']
    rtn = requests.get(api_url)
    rtns = json.loads(rtn.text)
    # print(api_url)
    return render_template('api.jinja2', title='API Calls', rtns=rtns, city=city)


if __name__ == '__main__':
    app.run(debug=True)
