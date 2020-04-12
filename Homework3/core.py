from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
import pickle

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.

API_KEY= '5s8t7yVuriiPmk_2o67eVK4WKa2tp4Ma95xaSNzU0lX_jpWj9ZayzDryUrj9uSqcVwUW2JhQWdehEjzlr7oNzwEH0ODwbf0oE2cG480FxHoaaI12RB8qzBd6yYxmXnYx'


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.



cuisine_arr = ['french','american','chinese']
allrestaurant = {}

for cuisine in cuisine_arr:
    term = cuisine
    # term = 'dinner'
    location = 'new york city'
    # location = 'San Francisco, CA'
    url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }
    curcnt = 0
    maxcnt = 1000
    cnt = 0
    while(curcnt<maxcnt):
        url_params = {
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': 50,
            'offset': curcnt
        }
        response = requests.request('GET', url, headers=headers, params=url_params).json()
        businesses = response.get('businesses')
        if not businesses:
            print(u'No businesses for {0} in {1} found.'.format(term, location))
            print ("this is for cnt {0} in {1}".format(curcnt,term))
            break
        #print (len(businesses))
        for i in range(len(businesses)):
            cnt +=1
            business_id = businesses[i]['id']
            #print (business_id)
            business_path = BUSINESS_PATH + business_id
            businessurl = '{0}{1}'.format(API_HOST, quote(business_path.encode('utf8')))
            businessres = requests.request('GET', businessurl, headers=headers, params={}).json()
            businessres['cuisine']=term
            if business_id not in allrestaurant:
                allrestaurant[business_id]=businessres
            print(businessres)
        print ("for term ",term, " cur cnt is ", cnt )
        curcnt+=50

with open('./allrestaurant.pickle','wb') as f:
    pickle.dump(allrestaurant,f)
