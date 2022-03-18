import tweepy
import configparser
import pandas as pd
import config

# read configs


api_key = config.api_key
api_key_secret = config.api_key_secret

access_token = config.access_token
access_token_secret = config.access_token_secret

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class Linstener(tweepy.Stream):

    tweets = []
    limit = 1

    def on_status(self, status):
        self.tweets.append(status)
        # print(status.user.screen_name + ": " + status.text)

        if len(self.tweets) == self.limit:
            self.disconnect()





stream_tweet = Linstener(api_key, api_key_secret, access_token, access_token_secret)

# stream by keywords
keywords = ['2022', '#python']
limit=100
stream_tweet.filter(track=keywords)

# stream by users
# users = ['MehranShakarami', 'veritasium']
# user_ids = []

tweets = tweepy.Cursor(api.search_tweets, q=keywords, count=100, tweet_mode='extended').items(limit)

for keys in keywords:
    user_ids.append(api.get_user(screen_name=user).id)

stream_tweet.filter(follow=user_ids)

# create DataFrame

columns = ['User', 'Tweet']
data = []

for tweet in stream_tweet.tweets:
    if not tweet.truncated:
        data.append([tweet.user.screen_name, tweet.text])
    else:
        data.append([tweet.user.screen_name, tweet.extended_tweet['full_text']])

df = pd.DataFrame(data, columns=columns)

print(df)