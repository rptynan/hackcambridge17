import sys, os, requests, collections, json, datetime
sys.path.append(os.path.abspath('..'))
from hackcambridge17.api_keys import SKYSCANNER_KEY
from geopy.distance import great_circle

def parse_coords(json_coords):
    split = json_coords.split(',')
    #print(split)
    latitude = float(split[0])
    longitude = float(split[1])

    return latitude, longitude

# get all airports
all_url = "http://partners.api.skyscanner.net/apiservices/geo/v1.0?apiKey=" + SKYSCANNER_KEY
all_airports = requests.get(all_url)
airports_json = all_airports.json()

# dates
leave_date = datetime.date.today() + datetime.timedelta(days = 2)

def find_airports(trump_loc, total_return=100):
    airport_dict = {}

    num_continents = len(airports_json["Continents"])
    num_countries = 0
    num_cities = 0
    num_aiports = 0
    for continent in range(num_continents):
        num_countries = len(airports_json["Continents"][continent]["Countries"])
        for country in range(num_countries):
            num_cities = len(airports_json["Continents"][continent]["Countries"][country]["Cities"])
            for city in range(num_cities):
                num_aiports = len(airports_json["Continents"][continent]["Countries"][country]["Cities"][city]["Airports"])
                for airport in range(num_aiports):
                    # Get distance from Trump for the airport
                    airport_coords = airports_json["Continents"][continent]["Countries"][country]["Cities"][city]["Airports"][airport]["Location"]
                    latitude, longitude = parse_coords(airport_coords)
                    airport_location = (longitude, latitude)
                    distance = great_circle(airport_location, trump_loc).miles

                    # Add airport data to dictionary with distance as key

                    airport_dict.update({distance : airports_json["Continents"][continent]["Countries"][country]["Cities"][city]["Airports"][airport]})

    # Sort flights by key (distance) in ascending order
    ordered_flights = collections.OrderedDict(sorted(airport_dict.items()))
    # Return number of results specified by 'total_return'
    return list(ordered_flights.items())[-total_return:]

def find_flights(trump_loc, my_loc, total_return=5):
    poss_airports = find_airports(trump_loc)
    flights = []
    for airport in poss_airports:
        url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{country}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}'.format(country = 'GB', currency = 'GBP', locale = 'gb-EN', originPlace = 'LHR', destinationPlace = airport[1]["Id"], outboundPartialDate = leave_date, inboundPartialDate = '', apiKey = SKYSCANNER_KEY )
        req = requests.get(url)
        quote_json = req.json()
        if quote_json["Quotes"]:
            airport[1].update({"Quotes": quote_json["Quotes"]})
            flights.append(airport)
    return flights

find_flights((38.9072, -77.0369), (51.5074, -0.1278), 5)
        
