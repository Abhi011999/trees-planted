from bs4 import BeautifulSoup as BS
import urllib.request
import tweepy
import time
from os import environ
previous = 0

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
print('API authenticated')

while (True):
    html = urllib.request.urlopen("https://www.teamtrees.org/")
    print('url opened')
    soup = BS(html, "html.parser")
    count = int(soup.findAll('div', {'id': 'totalTrees'})[0].get('data-count').strip())
    print(count)
    percent = round(float((count / 20000000) * 100), 1)
    print(percent)

    if percent > previous:
        tweet = str(count) + "/" + "20000000 (" + str(percent) + "%) Trees Planted #TeamTrees teamtrees.org"
        print(tweet)
        status = api.update_status(tweet)
        print(status)
        previous = percent
    time.sleep(10)