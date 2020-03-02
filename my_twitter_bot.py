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

import json
import time, random
from keys import *
import tweepy

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# possible text memes formats to search for: 
    # "oh to be", 
    # "no existe, no puede hacerte daño", 
    # "you vs the guy she told you not to worry about", 


def search_tweets():
    # devuelve un list los tweets que coincidan con el término de búsqueda.
    tl_tweets = api.search("coronavirus", count=1000)
    print("found", len(tl_tweets), "tweets\n")

    # cada item de la lista es un objeto status, cuyos parámetros son
    # accesibles como cualquier objeto
    for tw in tl_tweets[50:]: # printeamos el texto de los 50 últimos tuits junto con sus favs
        print(tw.text, "| favs:", tw.favorite_count)
        print("\n____________________\n")


if __name__ == "__main__":
    search_tweets()
