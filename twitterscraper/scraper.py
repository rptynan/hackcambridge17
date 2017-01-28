#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.abspath('..'))
from hackcambridge17.api_keys import TWITTER_KEYS

print(TWITTER_KEYS)

import json
import requests
from requests_oauthlib import OAuth1

payload = {'screen_name': 'potus', 'count': '30', 'exclude_replies': 'true'}
auth = OAuth1(TWITTER_KEYS['consumer_key'], TWITTER_KEYS['consumer_secret'], TWITTER_KEYS['access_token'], TWITTER_KEYS['access_secret'])
r = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json', params=payload, auth=auth)

tweets_json = r.json()

for i in range(30):
    print(tweets_json[i]["text"])
    print("location:")
    if tweets_json[i]["place"] is not None:
        print(tweets_json[i]["place"]["name"])
    else:
        print("unknown")
    print(tweets_json[i]["user"]["id"])
    print('\n')
