import os
from dotenv import load_dotenv, find_dotenv
# load_dotenv()
import requests
import json
import tweepy
from nltk.tokenize import WordPunctTokenizer
import re
from bs4 import BeautifulSoup
from textblob import TextBlob, Word, Blobber
from telegram import ParseMode
load_dotenv(find_dotenv())

token= os.environ.get('telegram_twitter_listener_key')
consumer_key= os.environ.get('twitter_api_key')
consumer_secret= os.environ.get('twitter_api_secret')
access_token= os.environ.get('twitter_access_token')
access_token_secret= os.environ.get('twitter_access_token_secret')

botsUrl= "https://api.telegram.org/bot{}".format(token)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def clean_tweets(twt):
    # twt = re.sub('#ethereum', 'ethereum', twt)
    # twt = re.sub('#Ethereum', 'Ethereum', twt)
    token = WordPunctTokenizer()  
    twt = re.sub('#[A-Za-z0-9]+ ','', twt) #removes any string with a '#' character
    twt = re.sub('\\n', '', twt)
    twt = re.sub('&;','and',twt)
    twt = re.sub('@[A-Za-z0-9]+ ','', twt)
    twt = re.sub('https?:\/\/\S+','',twt) #Removes any hyperlinks
    regex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    twt = re.sub(regex_pattern,'',twt)
    pattern = re.compile(r'(https?://)?(www\.)?(\w+\.)?(\w+)(\.\w+)(/.+)?')
    twt = re.sub(pattern,'',twt)
    re_list = ['@[A-Za-z0-9_]+', '#']
    combined_re = re.compile( '|'.join( re_list) )
    twt = re.sub(combined_re,'',twt)
    del_amp = BeautifulSoup(twt, 'lxml')
    del_amp_text = del_amp.get_text()
    del_link_mentions = re.sub(combined_re, '', del_amp_text)
    del_emoticons = re.sub(regex_pattern, '', del_link_mentions)
    lower_case = del_emoticons.lower()
    words = token.tokenize(lower_case)
    result_words = [x for x in words if len(x) > 2]
    return (" ".join(result_words)).strip()

def subjectivity(twt):
    return TextBlob(twt).sentiment.subjectivity

#Function to get the polarity

def getPolarity(twt):
    return TextBlob(twt).sentiment.polarity

def getSentiment(score):
    if score<0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

def giveUpdate(offset=None):
	url = botsUrl+ "/getupdates?timeout=100"
	if offset:
		url = botsUrl+ "/getupdates?offset={}&timeout=100".format(offset+1)
	resp= requests.get(url)
	return json.loads(resp.content)

def sendMessage(msg, chat_id):
	url= botsUrl+ "/sendMessage?chat_id={}&text={}&parse_mode={parse_mode}".format(chat_id,msg,parse_mode = ParseMode.HTML)
	resp= requests.get(url)
	return "sent message"


def getReply(msg):
    tweets= tweepy.Cursor(api.search, q= "#{} -filter:retweets".format(msg)).items(5)
    all_tweet= []
    for tw in tweets:
        screen_name = tw.user.screen_name
        text = tw.text
        id = str(tw.id)
        hyperlink =  "<a href='https://twitter.com/twitter/statuses/"+id+"'><b>"+screen_name+"</b></a>"
        sentiment = getSentiment(getPolarity(text))
        finalTweet = hyperlink+' - '+text+' -- '+sentiment
        all_tweet.append(finalTweet)
    return all_tweet



id_=None
while True:
	update= giveUpdate(offset=id_)
	update= update['result']

	if update:
		for item in update:
			id_= item['update_id']
			msg= item['message']['text']
			chat_id= item['message']['from']['id']
			if msg:
				reply= getReply(msg)
				for tw in reply:
					print(sendMessage(tw, chat_id))