import my_twitter_bot
import textprocessing
import pickle
import os
import k_means
import random
from pprint import pprint

def save_tweets(tweets, filename):
    pickle.dump(tweets, open("{}.p".format(filename), "wb"))

def load_tweets(filename):
    return pickle.load(open("{}.p".format(filename), "rb"))


words = ["coronavirus", "trump", "recession", "nintendo", "8m"]

tweets_saved = False

if os.path.exists('-'.join(words)+"_v2.p"):
    print("Tweets loaded from disk")
    tweets = load_tweets('-'.join(words)+"_v2")
else:
    tweets = my_twitter_bot.search_tweets(words)
    save_tweets(tweets, '-'.join(words)+"_v2")

documents = [
    'coronavirus haha coronavirus ayy lol el coronavirus me cago me cago',
    'coronavirus sdflk dasdfl coronavirus asdlk as ayyyyy caca',
    'asdlkf coronavirus ad coronavirus',
    'asdf coronavirus coronavirus ajajjaja caca',
    'sadfasdflkasdcoronavirus sldfasd coronavirus',
    'fasldkf coronavirus sldkfa k coronavirus coronavirus',
    'chochete peludo me apasiona comer chochete lo amo',
    'chochete jaja todos los días comer chochete',
    'chochete apasiona ajjaj chochete chochete',
    'trump, is trump and trump alsk da trumplka',
    'trump is a trump trump',
    'trump trump trump trump trump'
]

random.shuffle(tweets)

sparse_matrix = textprocessing.word2vec(tweets)


k_groups = k_means.k_means(sparse_matrix, 5)

for group in k_groups:
    print("\n\nGROUP\n\n")
    for index in group:
        print(index, "-->", tweets[index][1])
