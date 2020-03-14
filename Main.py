import twitterAPI
import textprocessing
import pickle
import os
import random
from pprint import pprint
import ClusteringAlgorithms

def save_tweets(tweets, filename):
    pickle.dump(tweets, open("{}.p".format(filename), "wb"))

def load_tweets(filename):
    return pickle.load(open("{}.p".format(filename), "rb"))


words = ["coronavirus", "trump", "recession", "nintendo", "8m"]

tweets_path = "serialized_tweets"

if os.path.exists(os.path.join(tweets_path, '-'.join(words)+"_v2.p")):
    print("Tweets loaded from disk")
    tweets = load_tweets(os.path.join(tweets_path, '-'.join(words)+"_v2"))
else:
    tweets = twitterAPI.search_tweets(words)
    save_tweets(tweets, os.path.join(tweets_path, '-'.join(words)+"_v2"))


random.shuffle(tweets)

sparse_matrix = textprocessing.word2vec(tweets)

result, noise_pts = ClusteringAlgorithms.bdscan(sparse_matrix)

# k_groups = ClusteringAlgorithms.k_means(sparse_matrix, 5)

for group in result:
    print("\n\nGROUP\n\n")
    for index in group:
        print(index, "-->", tweets[index][1])
