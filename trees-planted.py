from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen
import tweepy
import time
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api

    def on_status(self, tweet):
        if (tweet.text.find('#TeamTrees') != -1):
            print(tweet.user.name, " : ", tweet.text)
            reply = str("@" + tweet.user.screen_name + " https://twitter.com/TeamTrees6/status/" + api.user_timeline(exclude_replies=True, include_rts=False)[0].id_str)
            print("Replying to - " + tweet.user.name)
            print(api.update_status(status=reply, in_reply_to_status_id=tweet.id))
        return True

    def on_error(self, status_code):
        print("Got an error with code: ", str(status_code))
        return True

    def on_timeout(self):
        print("Timeout...")
        return True

def get_list(api):
    bot_followers = api.followers_ids()
    bot_friends = api.friends_ids() 
    for i in range(0, len(bot_followers)):
        bot_followers[i] = str(bot_followers[i])
    for i in range(0, len(bot_friends)):
        bot_friends[i] = str(bot_friends[i])
    final_list = bot_followers + bot_friends
    return final_list

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

final_list = get_list(api)
listener = StreamListener(api)
stream = tweepy.Stream(api.auth, listener)
stream.filter(follow=final_list, is_async=True)

while (True):
    req = Request("https://www.teamtrees.org/", headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
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