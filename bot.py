# bot.py

import tweepy
from secrets import *
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageFile
import random

ImageFile.LOAD_TRUNCATED_IMAGES = True

#Creating an OAuthHandler instance
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

#Construct the API instance
api = tweepy.API(auth)

def tweet_image(url, username, status_id):
    filename = 'temp.png'
    #Send a GET request
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        i = Image.open(BytesIO(request.content))
        i.save(filename)
        scramble(filename)
        api.update_with_media('scramble.png', status='@{0}'.format(username), in_reply_to_status_id=status_id)
        print("tweeted successfully")
    else:
        print('Unable to download image')

def scramble(filename):
    BLOCKLEN = 128
    img = Image.open(filename)
    width, height = img.size
    xblock = width // BLOCKLEN
    yblock = height // BLOCKLEN

    blockmap = [(xb * BLOCKLEN, yb * BLOCKLEN, (xb+1) * BLOCKLEN, (yb+1) * BLOCKLEN) for xb in range(xblock) for yb in range(yblock)]

    shuffle = list(blockmap)

    random.shuffle(shuffle)

    result = Image.new(img.mode, (width, height))
    for box, sbox in zip(blockmap, shuffle):
        # Returns a rectangular region from this orignal image
        crop = img.crop(sbox)
        # Pastes the cropped pixel into the new image object
        result.paste(crop, box)
        result.save('scramble.png')

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
