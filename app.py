#!/usr/bin/env python3
from api_keys import GOOGLE_KEY
from flask import Flask, render_template, request
from twitterscraper.scraper import init_twitter_scraper, get_location
from locationgetter.get_furthest_airport import find_flights
import json
import threading

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
    for lng, lat in bounds:  # Twitter's lng/lat order
        rlat += lat
        rlng += lng
    rlat /= len(bounds)
    rlng /= len(bounds)
    res = {'lat': rlat, 'lng': rlng}
    return json.dumps(res) if dojson else res


@app.route('/flightlocations')
def flightlocations():
    payload = json.loads(request.args['json'])
    our_loc = (payload['our_location']['lat'], payload['our_location']['lng'])
    trump_loc = \
        (payload['trump_location']['lat'], payload['trump_location']['lng'])

    flights_list = find_flights(trump_loc, our_loc, 5)
    flights_dict_list = []

    for item in flights_list:
        item_dict = item[1]
        item_dict['Distance'] = round(1.60934 * item[0])  # km
        item_dict['lng'], item_dict['lat'] = item_dict['Location'].split(', ')
        item_dict['lng'] = float(item_dict['lng'])
        item_dict['lat'] = float(item_dict['lat'])
        item_dict['price'] = round(item_dict['Quotes'][0]['MinPrice'])
        item_dict['co2e'] = round(0.101 * item_dict['Distance'])  # kg
        flights_dict_list.append(item_dict)
        print(item_dict)

    return json.dumps(flights_dict_list)


if __name__ == "__main__":
    threading.Thread(target=init_twitter_scraper).start()
    app.run(debug=True)
    app.run()
