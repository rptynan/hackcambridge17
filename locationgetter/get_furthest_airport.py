import sys, os, requests
sys.path.append(os.path.abspath('..'))
from hackcambridge17.api_keys import SKYSCANNER_KEY
from geopy.distance import great_circle

def parse_coords(json_coords):
	split = json_coords.split(',')
	#print(split)
	longitude = float(split[0])
	latitude = float(split[1])

	return longitude, latitude

trump_location = (-8.581021, -54.118652) #TODO fix this

antipode = (8.581021, 125.881348)

# get all airports
all_url = "http://partners.api.skyscanner.net/apiservices/geo/v1.0?apiKey=" + SKYSCANNER_KEY
all_airports = requests.get(all_url)

#print(all_airports.text)

airports_json = all_airports.json()
#print(airports_json["Continents"][0]["Countries"][0]["Cities"][0]["Airports"][0]["Location"])

num_continents = len(airports_json["Continents"])
#print(num_continents)



furthest_distance = 0
furthest_airport = ""

num_countries = 0
num_cities = 0
num_aiports = 0
for continent in range(num_continents):
	#print("Continent loop ------------------------------------------------------------------ ")
	num_countries = len(airports_json["Continents"][continent]["Countries"])
	#print(num_countries)
	for country in range(num_countries):
		#print("Country loop ------------------------------------------------------------------")
		num_cities = len(airports_json["Continents"][continent]["Countries"][country]["Cities"])
		#print(num_cities)
		for city in range(num_cities):
			#print("City loop ------------------------------------------------------------------")
			num_aiports = len(airports_json["Continents"][continent]["Countries"][country]["Cities"][city]["Airports"])
			#print(num_aiports)
			for airport in range(num_aiports):
				airport_coords = airports_json["Continents"][continent]["Countries"][country]["Cities"][city]["Airports"][airport]["Location"]
				#print(airport_coords)
				longitude, latitude = parse_coords(airport_coords)
				#print(longitude)
				#print(latitude)
				airport_location = (longitude, latitude)

				distance = great_circle(airport_location, trump_location).miles

				if distance >= furthest_distance:
					furthest_distance = distance
					furthest_airport_name = airports_json["Continents"][continent]["Countries"][country]["Cities"][city]["Airports"][airport]["Name"]
					furthest_airport_id = airports_json["Continents"][continent]["Countries"][country]["Cities"][city]["Airports"][airport]["Id"]


print(furthest_distance)
print(furthest_airport_name)
print(furthest_airport_id)

print(great_circle(antipode, trump_location).miles)

#TODO return furthest airport



# set up the inflow (trump loc) and outflow (airport)