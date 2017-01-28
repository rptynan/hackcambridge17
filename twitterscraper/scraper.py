#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.abspath('..'))
from hackcambridge17.api_keys import TWITTER_KEYS

print(TWITTER_KEYS)

import json
import requests
from requests_oauthlib import OAuth1

payload = {'screen_name': 'potus', 'count': '30', 'exclude_replies': 'true'}
auth = OAuth1(TWITTER_KEYS['consumer_key'], 'BOGAKvC9vVvHjJXGIWkLJqpPlZ3mzCvS5bT0HuBUdRaNvcMPZ6', '90660166-D62ACDdJyz669gs9P70zuA3aG0AmuCBOE556UYRTG', 'Zzmjxpw3GcF7ViHdebW9WxYpUH8CR15G50inAkSGjDv4J')
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
