# lista de atributos que tiene un tuit:
    # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
    # '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__',
    # '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
    # '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
    # '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
    # '_api', '_json', 'author', 'contributors', 'coordinates', 'created_at',
    # 'destroy', 'entities', 'favorite', 'favorite_count', 'favorited', 'geo',
    # 'id', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
    # 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str',
    # 'is_quote_status', 'lang', 'metadata', 'parse', 'parse_list', 'place',
    # 'possibly_sensitive', 'quoted_status', 'quoted_status_id',
    # 'quoted_status_id_str', 'retweet', 'retweet_count', 'retweeted',
    # 'retweets', 'source', 'source_url', 'text', 'truncated', 'user']

# lista de atributos de un tuit extendido:
    # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', 
    # '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', 
    # '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', 
    # '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 
    # '__weakref__', '_api', '_json', 'author', 'contributors', 'coordinates', 'created_at', 
    # 'destroy', 'display_text_range', 'entities', 'extended_entities', 'favorite', 'favorite_count', 
    # 'favorited', 'full_text', 'geo', 'id', 'id_str', 'in_reply_to_screen_name', 
    # 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 
    # 'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'metadata', 'parse', 'parse_list', 
    # 'place', 'possibly_sensitive', 'retweet', 'retweet_count', 'retweeted', 'retweets', 'source', 
    # 'source_url', 'truncated', 'user']

import json
import time, random
from keys import *
import tweepy
from textprocessing import word2vec, cosine_similarity
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import re
import pickle

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# possible text memes formats to search for: 
    # "oh to be", 
    # "no existe, no puede hacerte daño", 
    # "you vs the guy she told you not to worry about", 


def get_full_text(status):
    if 'retweeted_status' in status._json:
        return status._json['retweeted_status']['full_text']
    else:
        return status.full_text

def search_tweets(words):
    # devuelve un list los tweets que coincidan con el término de búsqueda.

    tweets = []
    for word in words:
        tl_tweets = api.search(word , lang='en', tweet_mode='extended', count=100)
        for tweet in tl_tweets:
            tweet = get_full_text(tweet)
            tweet = re.sub(r'http\S+',"", tweet)
            tweets.append(tweet)


    return tweets

# def tokenize_tweets(tweets):
#     from nltk import RegexpTokenizer
#     tokenizer = RegexpTokenizer("\w+\'\w+|\w+")
#     new_tweets = []
#     for tweet in tweets:
#         tweet_tokens = tokenizer.tokenize(tweet)
#         tweet_tminus = [x.lower() for x in tweet_tokens]
#         new_tweets.append(tweet_tminus)
#     return new_tweets


# if __name__ == "__main__":
#     # search_tweets(["coronavirus"])
#
#     list = ["hola me llamo aLex","aa patata hola"]
#     a = tokenize_tweets(list)
#     print(a)

