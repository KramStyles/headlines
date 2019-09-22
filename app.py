from flask import Flask, render_template, request, make_response
import feedparser
import json, urllib, requests, datetime
import urllib.request
import urllib.parse

app = Flask(__name__)

rssFeeds = {
    'iol': 'http://www.iol.co.za/cmlink/1.640',
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
}

DEFAULTS = {
    'article': 'bbc',
    'city': 'Enugu',
    'api_key': '7826b779b9c7e0768b8f1a46228110a3',
    'curr_key': '607aab47547941a49d8085e68c835749',
    'curr_from': 'NGN',
    'curr_to': 'USD'
}


@app.route('/')
@app.route('/<article>')
def index(article='bbc'):
    feed = feedparser.parse(rssFeeds[article])
    # first = feed['entries'][0]
    return render_template('home.jinja2', header=article, title=article.upper() + ' News Feed',
                           newsFeeds=feed['entries'])


@app.route('/request')
def getNews():
    query = request.args.get('agency')
    if not query or query.lower() not in rssFeeds:
        agency = DEFAULTS['article']
    else:
        agency = query.lower()
    city = request.args.get('city')
    if not city:
        city = request.cookies.get("city")
        if not city:
            city = DEFAULTS['city']
    api_url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric&appid=" + DEFAULTS['api_key']
    rtn = requests.get(api_url)
    rtns = json.loads(rtn.text)
    curr, value = getCurrency()
    currFrom = request.args.get('currFrom')
    if not currFrom:
        currFrom = request.cookies.get('currFrom')
        if not currFrom:
            currFrom = DEFAULTS['curr_from']
    currTo = request.args.get('currTo')
    if not currTo:
        currTo = request.cookies.get('currTo')
        if not currTo:
            currTo = DEFAULTS['curr_to']
    value1 = value.get(currFrom)
    value2 = value.get(currTo)
    value11 = value1 / value2
    value = currFrom + ' TO ' + currTo
    feed = feedparser.parse(rssFeeds[agency])
    # weather = myGetWeather(city)
    response = make_response(render_template('request.jinja2', header=agency, title=agency.upper() + 'NewsFeed Request',
                                             newsFeeds=feed['entries'], rtns=rtns, city=city, curr=curr, value=value,
                                             currValue=value11,
                                             currFrom=currFrom, currTo=currTo))
    expires = datetime.datetime.now() + datetime.timedelta(days=31)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currFrom", currFrom, expires=expires)
    response.set_cookie("currTo", currTo, expires=expires)
    return response


def getCurrency():
    api_url = "https://openexchangerates.org/api/latest.json?app_id=" + DEFAULTS['curr_key']
    rtn = requests.get(api_url)
    rtns = json.loads(rtn.text)
    value = json.loads(rtn.text).get('rates')
    return rtns, value


def myGetWeather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q=" + query + "&units=metric&appid=" + DEFAULTS['api_key']
    rtn = requests.get(api_url)
    rtnss = json.loads(rtn.text)
    return rtnss


def getWeather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q=aba&units=metric&appid=7826b779b9c7e0768b8f1a46228110a3'
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {
            "Description": parsed['weather'][0]['description'],
            "Temperature": parsed['main']['temp'],
            "City": parsed['name']
        }
    return weather


@app.route('/3d')
def d():
    return render_template('3dTransforms.jinja2')


if __name__ == '__main__':
    app.run(debug=True)
