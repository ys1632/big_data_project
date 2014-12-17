from TwitterAPI import TwitterAPI, TwitterRestPager
from datetime import datetime, date
import bitly_api
import urllib2, json
import httplib

from pymongo import MongoClient

connection = MongoClient()

db = connection['foursquare']

col = db.create_collection('check_in', capped=True,size=200000)



SEARCH_TERM = "4sq.com"

CONSUMER_KEY = 'yp0Onn7MprXj5IZDaOL57dyvQ'
CONSUMER_SECRET = 'L4KDkeFlvJM3u3208VgXZ3gTiaWlGOtKvjIqhvNIAoPcYZ7yfs'
ACCESS_TOKEN_KEY = '2321306595-G9Qr4XmivVfyTuqLKmadZxLVlyL9OgyV4HgxNIZ'
ACCESS_TOKEN_SECRET = '0tX8VhWOioxJ3fQtThAHKolhkbDPS5UtRSfjteyZJQdix'


BITLY_USERNAME = 'o_p00h7vd5h'
BITLY_API_KEY = 'R_19bff5294a094749a4177d9f639b7637'
BITLY_ACCESS_TOKEN = 'c6869fe932e2b5b912d97382c885fb8df8ba2bd8'

FOURSQUARE_ACCESS_TOKEN = 'K44DQZABARQM2HM2ETXZZHLXY11KYXAHAKY3NB0BN15KBN0Z'


api = TwitterAPI(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)

bitly = bitly_api.Connection(access_token = BITLY_ACCESS_TOKEN)


pager = TwitterRestPager(api, 'search/tweets', {'q': SEARCH_TERM})

def get_checkid_and_s(url):
    checkin_index = url.find('checkin')
    mark_s_index = url.find('?s=')
    check_id = url[checkin_index + 8: mark_s_index]
    refer_ref_index = url.find('&ref')
    signature_id = url[mark_s_index + 3: refer_ref_index]
    return check_id, signature_id

def get_check_in_info(id, sig):
    dt = date.today()
        
    url = "https://api.foursquare.com/v2/checkins/" + id + '?signature=' + sig + '&oauth_token=' + FOURSQUARE_ACCESS_TOKEN + '&v=' + dt.strftime('%Y%m%d')
        #	print url
    data = json.load(urllib2.urlopen(url))
    checkin = data['response']['checkin']
    date_info = checkin['createdAt']
    timezoneoffset = checkin['timeZoneOffset']
    user_id = checkin['user']['id']
    location = checkin['venue']['location']
    lat = location['lat']
    lng = location['lng']
    categories = checkin['venue']['categories'][0]
    categories_name = categories['name']
    temp = {'lat': lat, 'lng': lng, 'categories_name':str(categories_name)}
    col.insert(temp)
    print temp


for item in pager.get_iterator():
    if 'entities' in item:
        for url in item['entities']['urls']:
            try:
                if '4sq.com' in url['expanded_url']:
                    data = bitly.expand(shortUrl=url['expanded_url'])
                    if 'error' not in data[0]:
                        a, b = get_checkid_and_s(data[0]['long_url'])
                        get_check_in_info(a, b)
            except urllib2.HTTPError, e:
                pass
            except urllib2.URLError, e:
                pass
            except httplib.HTTPException, e:
                pass
            except Exception:
                import traceback
                pass

