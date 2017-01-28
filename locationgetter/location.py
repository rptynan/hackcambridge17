#!/usr/bin/env python3
import sys, os, requests
sys.path.append(os.path.abspath('..'))
from hackcambridge17.api_keys import MICROSOFT_KEY



headers = {
    # Request headers
    'Content-Type': 'text/plain',
    'Ocp-Apim-Subscription-Key': MICROSOFT_KEY,
}

url = "https://westus.api.cognitive.microsoft.com/entitylinking/v1.0/link?"
data = "Donald Trump is in London"

r = requests.post(url, data=data, headers=headers)
print(r.text)

# check data includes Donald Trump? 


# check data includes location


