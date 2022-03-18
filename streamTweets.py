from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import config
import json
import logging
import tweepy
import config
import logging
from telegram.ext.updater import Updater
from telegram.update import Update
import telegram
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler

logger = logging.getLogger(__name__)

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(config.api_key, config.api_secret_key)
        auth.set_access_token(config.access_token, config.access_token_secret)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, status, update: Update, context: CallbackContext):
        tweet = json.loads(status)
        tweet_text = tweet["text"]
        tweet_id = tweet["id"]
        chat_id = update.effective_chat.id
        # update.message.reply_text(tweet_text, chat_id)
        # update.message.reply_text(tweet_id, chat_id)
        update.send_message(
            chat_id, tweet_id, tweet_text
        )
        
        # tweet_url = f"https://twitter.com/twitter/statuses/{tweet_id}"
        # try:
            
        #     bot.send_message(
        #         chat_id = "1443973207",
        #         text = tweet_text
        #         )
        #     print('sent')
        # except:
        #     logger.error("faild forwarding tweet to channel")
        print(tweet_text,tweet_id)
    
    
    
        
    # def send_msg(update: Update, context: CallbackContext):
    #     chat_id = update.effective_chat.id
    #     print(chat_id)
    #     update.message.reply_text(tweet)
        

    def on_error(self, status):
        print(status)

 
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["#ROE","#RETH","#Realms of ethernity","#Realms of ethernity scam"]
    fetched_tweets_filename = "tweets1.txt"
    token = "5236830904:AAHjxyq08dXuJzKofXmPkJ30X5V1lNOUhIc"
    updater = Updater(token = token, use_context=True)
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    # updater.dispatcher.add_handler(CommandHandler('start',StdOutListener.on_data))
    updater.start_polling()
    updater.idle()
