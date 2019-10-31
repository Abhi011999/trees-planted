from bs4 import BeautifulSoup as BS
import urllib.request
import tweepy
import time
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

while (True):
    html = urllib.request.urlopen("https://www.teamtrees.org/")
    last = open("last.txt", "r+")
    previous = int(last.read(4).replace('.', ''))
    soup = BS(html, "html.parser")
    count = int(soup.findAll('div', {'id': 'totalTrees'})[0].get('data-count').strip())
    percent = round(float((count / 20000000) * 100), 1)

    if int(str(percent).replace('.', '')) > previous:
        tweet = str(count) + "/" + "20000000 (" + str(percent) + "%) Trees Planted #TeamTrees teamtrees.org"
        print(tweet)
        status = api.update_status(tweet)
        print(status)
        last.close()
        last = open('last.txt', 'w+')
        previous = last.write(str(percent))
        last.close()
    else:
        print('Percentage not updated')
        last.close()
    time.sleep(10)