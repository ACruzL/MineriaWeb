import twitterAPI
import textprocessing
import openpyxl as xls
import pickle
import os
import random
from pprint import pprint
import ClusteringAlgorithms
import EvaluationAlgorithms

def save_tweets(tweets, filename):
    pickle.dump(tweets, open("{}.p".format(filename), "wb"))

def load_tweets(filename):
    return pickle.load(open("{}.p".format(filename), "rb"))

def show_results(index_list):
    for group in index_list:
        print("\n\nGROUP\n\n")
        for index in group:
            print(index, "-->", tweets[index][1])

def save_to_excel(result_list):    
    try:
        workbook = xls.load_workbook(filename="output_execution_shell.xlsx")
        print("loaded workbook from disk")
    except:
        workbook = xls.Workbook()
    
    sheet = workbook.active

    sheet["B1"] = "ALGORITHMS"
    sheet["C1"] = "BDSCAN"
    sheet["D1"] = "K MEANS"
    sheet["E1"] = "K MEANS++"

    init_cell_row = 0
    for cell in sheet["B"]:
        if cell.value is None:
            init_cell_row = cell.row
            break
        else:
            init_cell_row = cell.row
    
    cols = ["C", "D", "E"]

    for alg_dict, col in zip(result_list, cols):
        offset = 1
        for item in alg_dict.items():
            eval_alg = item[0]
            score = item[1]
            sheet["B{}".format(init_cell_row + offset)] = eval_alg
            sheet["{}{}".format(col, init_cell_row + offset)] = score

            offset += 1

    workbook.save(filename="output_execution.xlsx")



words = ["coronavirus", "trump", "recession", "nintendo", "8m"]

tweets_path = "serialized_tweets"

if os.path.exists(os.path.join(tweets_path, '-'.join(words)+"_v2.p")):
    print("Tweets loaded from disk")
    tweets = load_tweets(os.path.join(tweets_path, '-'.join(words)+"_v2"))
else:
    tweets = twitterAPI.search_tweets(words)
    save_tweets(tweets, os.path.join(tweets_path, '-'.join(words)+"_v2"))


tweet_kmeans = tweets.copy()
tweet_k_plus = tweets.copy()

random.shuffle(tweets)
random.shuffle(tweet_kmeans)
random.shuffle(tweet_k_plus)

sparse_matrix_bdscan = textprocessing.word2vec(tweets)
sparse_matrix_kmeans = textprocessing.word2vec(tweet_kmeans)
sparse_matrix_k_plus = textprocessing.word2vec(tweet_k_plus)

bdscan, noise_pts = ClusteringAlgorithms.bdscan(sparse_matrix_bdscan)
k_groups = ClusteringAlgorithms.k_means(sparse_matrix_kmeans, 5)
k_plus_plus = ClusteringAlgorithms.k_means_plus_plus(sparse_matrix_k_plus, 5)

dist_matrix = ClusteringAlgorithms.distance_matrix(sparse_matrix)
bdscan_results = EvaluationAlgorithms.evaluate(bdscan, tweets, words, dist_matrix)
k_groups_results = EvaluationAlgorithms.evaluate(k_groups, tweets, words, dist_matrix)
k_plus_plus_results = EvaluationAlgorithms.evaluate(k_plus_plus, tweets, words, dist_matrix)

print("########## BDSCAN RESULTS ##########")
pprint(bdscan_results)
print()

print("########## K MEANS RESULTS ##########")
pprint(k_groups_results)
print()

print("########## K MEANS++ RESULTS ##########")
pprint(k_plus_plus_results)
print()

save_to_excel([bdscan_results, k_groups_results, k_plus_plus_results])


