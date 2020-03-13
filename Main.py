import my_twitter_bot
import textprocessing
import pickle

def save_tweets(tweets, filename):
    pickle.dump(tweets, open("{}.p".format(filename), "wb"))

def load_tweets(filename):
    return pickle.load(open("{}.p".format(filename), "rb"))


words = ["coronavirus", "trump", "recession", "nintendo", "8m"]

tweets_saved = False

if tweets_saved:
    tweets = load_tweets('-'.join(words))
else:
    tweets = my_twitter_bot.search_tweets(words)
    save_tweets(tweets, '-'.join(words))


sparse_matrix = textprocessing.word2vec(tweets)




print(sparse_matrix)
print(sparse_matrix.shape)