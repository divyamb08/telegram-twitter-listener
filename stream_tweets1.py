import matplotlib as plt
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import random
import config
from telegram.ext import Updater
import tweepy
import time
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request
from telegram import Update
from telegram.ext import CallbackContext
from nltk.tokenize import WordPunctTokenizer
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import logging
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
import requests

updater = Updater("5236830904:AAHjxyq08dXuJzKofXmPkJ30X5V1lNOUhIc",
                  use_context=True)

def get_data(tags):
    consumer_key = config.api_key
    consumer_secret = config.api_secret_key
    token_key = config.access_token
    token_secret = config.access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token_key, token_secret)
    api = tweepy.API(auth)
    stream.filter(track=tags)