from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

rssFeeds = {
    'iol': 'http://www.iol.co.za/cmlink/1.640',
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
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
        agency = 'bbc'
    else:
        agency = query.lower()
    feed = feedparser.parse(rssFeeds[agency])
    return render_template('request.jinja2', header=agency, title=agency.upper() + 'NewsFeed Request',
                           newsFeeds=feed['entries'])


if __name__ == '__main__':
    app.run(debug=True)
