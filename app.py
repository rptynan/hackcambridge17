#!/usr/bin/env python3
from flask import Flask, render_template
from api_keys import GOOGLE_KEY
from twitterscraper.scraper import init_twitter_scraper, get_location
import threading
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'layout.html',
        GOOGLE_KEY=GOOGLE_KEY,
    )


@app.route('/donaldslocation')
def donaldslocation():
    bounds = get_location()['bounding_box']['coordinates'][0]
    rlat = 0
    rlng = 0
    for lng, lat in bounds: # Twitter's lng/lat order
        rlat += lat
        rlng += lng
    rlat /= len(bounds)
    rlng /= len(bounds)
    return json.dumps({'lat': rlat, 'lng': rlng})


if __name__ == "__main__":
    threading.Thread(target=init_twitter_scraper).start()
    app.run(debug=True)
    app.run()
