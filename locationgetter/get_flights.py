import sys, os, requests, datetime
sys.path.append(os.path.abspath('..'))
from hackcambridge17.api_keys import SKYSCANNER_KEY

# import furthest airport
furthest_airport = 'CDG'

leave_date = datetime.date.today() + datetime.timedelta(days=2) 

#print(date_tomorrow)

url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{country}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}'.format(
	country = 'GB', currency = 'GBP', locale = 'gb-EN', originPlace = 'LHR', destinationPlace = furthest_airport, outboundPartialDate = leave_date, inboundPartialDate = '', apiKey = SKYSCANNER_KEY )

print(url)

req = requests.get(url)

print(req.text)