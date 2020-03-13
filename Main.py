import my_twitter_bot
import textprocessing
import pickle
import ClusteringAlgorithms
from pprint import pprint

def save_tweets(tweets, filename):
    pickle.dump(tweets, open("{}.p".format(filename), "wb"))

def load_tweets(filename):
    return pickle.load(open("{}.p".format(filename), "rb"))


# words = ["coronavirus", "trump", "recession", "nintendo", "8m"]
words = ["coronavirus"]

tweets_saved = True

if tweets_saved:
    tweets = load_tweets('-'.join(words))
else:
    tweets = my_twitter_bot.search_tweets(words)
    save_tweets(tweets, '-'.join(words))


sparse_matrix = textprocessing.word2vec(tweets)

result, noise_pts = ClusteringAlgorithms.bdscan(sparse_matrix)

pprint(result)