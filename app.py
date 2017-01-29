#!/usr/bin/env python3
from flask import Flask, render_template
from api_keys import GOOGLE_KEY
from twitterscraper.scraper import init_twitter_scraper, get_location
from locationgetter.get_furthest_airport import find_airports
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
def donaldslocation(dojson=True):
    bounds = get_location()['bounding_box']['coordinates'][0]
    rlat = 0
    rlng = 0
    for lng, lat in bounds: # Twitter's lng/lat order
        rlat += lat
        rlng += lng
    rlat /= len(bounds)
    rlng /= len(bounds)
    res = {'lat': rlat, 'lng': rlng}
    return json.dumps(res) if dojson else res

@app.route('/airportlocations')
def airportlocations():
    trump_loc = donaldslocation(dojson=False)
    lng = trump_loc['lng']
    lat = trump_loc['lat']
    
    airport_list = find_airports((lat, lng), 5)
    airport_dict_list = []

    for item in airport_list:
        item_dict = item[1]
        item_dict['Distance'] = item[0]
        airport_dict_list.append(item_dict)

    return json.dumps(airport_dict_list)
    
    

if __name__ == "__main__":
    threading.Thread(target=init_twitter_scraper).start()
    app.run(debug=True)
    app.run()

airportlocations()
