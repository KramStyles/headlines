from flask import Flask
import feedparser

app = Flask(__name__)

rssFeeds = {
    'newsFeed': 'http://feeds.bbci.co.uk/news/rss.xml',
    'iolFeed': 'http://www.iol.co.za/cmlink/1.640',
    'bbcFeed': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnnFeed': 'http://rss.cnn.com/rss/edition.rss',
    'foxFeed': 'http://feeds.foxnews.com/foxnews/latest',
}


def getNews(news):
    feed = feedparser.parse(rssFeeds[news])
    first = feed['entries'][0]
    return """
            <html>
                <body>
                    <h1>News Feed</h1>
                    <b><a href="{3}">{0}</a></b><br>
                    <b>Date Published: <u>{1}</u></b><br>
                    <p>{2}</p><br>
                </body>
            </html>
        """.format(first.get('title'), first.get('published'), first.get('summary'), first.get('link'))


@app.route('/')
@app.route('/bbc')
def bbc():
    return getNews('newsFeed')


@app.route('/cnn')
def cnn():
    return getNews('cnnFeed')


@app.route('/fox')
def fox():
    return getNews('foxFeed')


@app.route('/iol')
def buzz():
    return getNews('iolFeed')


if __name__ == '__main__':
    app.run(debug=True)
