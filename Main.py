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

def show_results(index_list):
    for group in index_list:
        print("\n\nGROUP\n\n")
        for index in group:
            print(index, "-->", tweets[index][1])


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

k_groups = ClusteringAlgorithms.k_means(sparse_matrix, 5)

k_plus_plus = ClusteringAlgorithms.k_means_plus_plus(sparse_matrix, 5)


print("\n\n\n##### BDSCAN #####\n\n\n")
show_results(result)

print("\n\n\n##### K MEANS #####\n\n\n")
show_results(k_groups)

print("\n\n\n##### K MEANS ++ #####\n\n\n")
show_results(k_plus_plus)