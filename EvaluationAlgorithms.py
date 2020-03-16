import numpy as np

def randIndex(clusters, tweets, classes, tweets_per_class=100):
    numTweets = len(tweets)
    class_dict = {k: v for v, k in enumerate(classes)}
    total_true_positives = 0
    total_false_positives = 0
    total_false_negatives = 0

    for cluster in clusters:
        numTweetsCluster = len(cluster)
        true_positives = 0
        class_count = np.zeros(len(classes))
        for x in range(len(cluster)):
            tweet = cluster[x]
            current_class = tweets[tweet][1]
            class_count[class_dict[current_class]] += 1
            for y in range(x+1, len(cluster)):
                if current_class == tweets[cluster[y]][1]:
                    true_positives += 1

        #True positives
        total_true_positives += true_positives

        #False positives
        false_positives = ((numTweetsCluster * (numTweetsCluster-1))/2) - true_positives
        total_false_positives += false_positives

        #False negatives
        false_negatives = 0
        for tweets_in_cluster in class_count:
            false_negatives += (tweets_in_cluster * (tweets_per_class - tweets_in_cluster))
        total_false_negatives += false_negatives/2

    num_pairs = (numTweets * (numTweets-1))/2

    total_true_negatives = num_pairs - total_true_positives - total_false_negatives - total_false_positives

    print("--------------------------------")
    print("RandIndex: ",total_true_positives, total_false_negatives, total_true_negatives, total_false_positives)
    print("--------------------------------")

    rand_score = (total_true_negatives + total_true_positives) / num_pairs

    return rand_score

