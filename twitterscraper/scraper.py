#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.abspath('..'))
from hackcambridge17.api_keys import TWITTER_KEYS

import json
import requests
from requests_oauthlib import OAuth1

tweets_json = {}
num_tweets = 50
POTUS_ID = 822215679726100480
REALDONALDTRUMP_ID = 25073877

def init():
    payload = {'screen_name': 'potus', 'count': num_tweets, 'exclude_replies': 'true'}
    auth = OAuth1(TWITTER_KEYS['consumer_key'], TWITTER_KEYS['consumer_secret'], TWITTER_KEYS['access_token'], TWITTER_KEYS['access_secret'])
    r = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json', params=payload, auth=auth)
    global tweets_json
    tweets_json = r.json()

def get_recent_location():
    i = 0
    while (i < num_tweets and tweets_json[i]["place"] is None):
        i = i + 1
    if(i < num_tweets):
        return tweets_json[i]["place"]
    else:
        return None

def get_location_from_date(date):
    i = 0
    while (i < num_tweets and is_later(date, tweets_json[i]["created_at"])):
        i = i + 1
    
    while (i < num_tweets and tweets_json[i]["place"] is None):
        i = i + 1

    if(i < num_tweets):
        return tweets_json[i]["place"]
    else:
        return None

def is_later(goal_date, curr_date):
    gdj = date_to_JSON(goal_date)
    cdj = date_to_JSON(curr_date)

    goal_date_str = str(gdj["year"]) + str(gdj["month"]) + str(gdj["day"]) + str(gdj["hour"]) + str(gdj["minute"]) + str(gdj["seconds"])

    curr_date_str = str(cdj["year"]) + str(cdj["month"]) + str(cdj["day"]) + str(cdj["hour"]) + str(cdj["minute"]) + str(cdj["seconds"])

    if(int(curr_date_str > goal_date_str)):
        return True
    else:
        return False  

def date_to_JSON(date):
    my_json = {}
    date_array = date.split()
    time_array = date_array[3].split(":")
    my_json["month"] = convert_month(date_array[1])
    my_json["day"] = date_array[2]
    my_json["hour"] = time_array[0]
    my_json["minute"] = time_array[1]
    my_json["seconds"] = time_array[2]
    my_json["year"] = date_array[5]
    return my_json
    
def convert_month(month): 
    return {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }[month]

def print_tweets():
    for i in range(num_tweets):
        print(tweets_json[i]["text"])
        print("location:")
        if tweets_json[i]["place"] is not None:
            print(tweets_json[i]["place"])
        else:
            print("unknown")
        print(tweets_json[i]["user"]["id"])
        print(tweets_json[i]["created_at"])
        print('\n')
