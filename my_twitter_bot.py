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
    tl_tweets = api.search("meme", count=100)
    print("found", len(tl_tweets), "tweets")

    # el tipo de los tuits es un objeto Status. Lo pasamos a json...
    json_tweet = json.dumps(tl_tweets[0]._json)

    # de json lo pasamos a un dict de python, fácilmente accesible.
    dict_py = json.loads(json_tweet)

    # ahora simplemente podemos acceder al texto tal que así.
    print(dict_py['text'])

    # además hay infinitos parámetros para encontrar el número de favs 
    # de dicho tuit, numero de RTs, y otro montón de estadísticas, 
    # en caso de que fueran interesantes o necesarias.


if __name__ == "__main__":
    search_tweets()
