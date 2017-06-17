# bot.py

import tweepy
from secrets import *

#Creating an OAuthHandler instance
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_secret)

#Construct the API instance
api = tweepy.API(auth)

#Create a class inheriting from the tweepy StreamListener
class BotStreamer(tweepy.StreamListener):

    def on_status(self, status):
        username = status.user.screen_name
        status_id = status.id

        if 'media' in status.entities:
            for image in status.entities['media']:
                tweet_image(image['media_url'], username, status_id)

myStreamListener = BotStreamer()

#Construct the Stream instance
stream = tweepy.Stream(auth, myStreamListener)

stream.filter(track=['@mytweebot'])

