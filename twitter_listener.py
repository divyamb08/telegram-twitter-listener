from distutils.command.config import config
import os
import json
import logging
import tweepy
import config
import logging
from telegram.ext.updater import Updater
from telegram.update import Update
import telegram

consumer_key = config.api_key
consumer_secret = config.api_secret_key
access_token = config.access_token
access_token_secret = config.access_token_secret

auth = tweepy.OAuthHandler(
    consumer_key,
    consumer_secret
    )
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class MyListener(tweepy.Stream):
    def __init__(self):
        self.logger = logging.getLogger("MyListenerLogs")
        self.logger.setLevel(logging.DEBUG)
    def on_connect(self):
        self.logger.info("connected to stream !")
    def on_data(self, status):
        tweet = json.loads(status)
        tweet_text = tweet["text"]
        tweet_id = tweet["id"]
      
        tweet_url = f"https://twitter.com/twitter/statuses/{tweet_id}"
        try:
            bot = Bot(token = "5236830904:AAHjxyq08dXuJzKofXmPkJ30X5V1lNOUhIc")
            bot.send_message(
                chat_id = "1443973207",
                text = tweet_text
                )
        except:
            logger.error("faild forwarding tweet to channel")


def main():
    token = "5236830904:AAHjxyq08dXuJzKofXmPkJ30X5V1lNOUhIc"
    updater = Updater(token = token, use_context=True)
   
    listener = MyListener
    stream = tweepy.Stream(
        auth = api.auth, 
        listener = listener()
        )
    stream.filter(track = ["#ROE","#RETH","Realms of ethernity", "Realms of ethernity scam"])
 
    updater.start_polling()
    updater.idle()
    
if __name__ == "__main__":
    main()
    

