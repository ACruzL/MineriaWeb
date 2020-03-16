import numpy as np
import math
from multiprocessing.dummy import Pool

def confusionMatrix(clusters, tweets, classes, tweets_per_class):
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

    return {"true_positives":   total_true_positives,
            "false_positives":  total_false_positives,
            "false_negatives":  total_false_negatives,
            "true_negatives":   total_true_negatives}

def precision_recall(confusion_dict):

    precision = confusion_dict["true_positives"]/(confusion_dict["true_positives"] + confusion_dict["false_positives"])

    recall = confusion_dict["true_positives"]/(confusion_dict["true_positives"] + confusion_dict["false_negatives"])

    return precision, recall

def randIndex(confusion_dict, total_pairs):

    rand_score = (confusion_dict["true_negatives"] + confusion_dict["true_positives"]) / total_pairs

    return rand_score

def fowlkesMallowsScore(precision, recall):

    return math.sqrt(precision*recall)

def silhouetteScore(clusters, distance_matrix):
    def elementSilhouette(element, num_cluster):
        inside_similarity = 0
        outside_similarity = 0
        count = 0
        for num_cluster_aux in range(len(clusters)):
            if num_cluster == num_cluster_aux:
                for element_aux in clusters[num_cluster_aux]:
                    inside_similarity += distance_matrix[element][element_aux]
                inside_similarity /= (len(clusters[num_cluster_aux]) + 1)
            else:
                for element_aux in clusters[num_cluster_aux]:
                    outside_similarity += distance_matrix[element][element_aux]
                    count += 1
                    # print(distance_matrix[element][element_aux], element, element_aux)
        
        outside_similarity /= count
        silhouette = (outside_similarity - inside_similarity)/ max(outside_similarity, inside_similarity)
        return silhouette

    element_row = [(a, x) for x in range(len(clusters)) for a in clusters[x]]
    with Pool() as pool:
        silhouette_results = pool.starmap(elementSilhouette, element_row)

    return np.mean(silhouette_results)


def evaluate(clusters, tweets, classes, distance_matrix, tweets_per_class=100):
    numTweets = len(tweets)
    num_pairs = (numTweets * (numTweets-1))/2

    confusion_dict = confusionMatrix(clusters, tweets, classes, tweets_per_class)
    result_dict = {}

    #Algorithms
    result_dict["precision"], result_dict["recall"] = precision_recall(confusion_dict)
    result_dict["rand score"] = randIndex(confusion_dict, num_pairs)
    result_dict["fowlkesmallows score"] = fowlkesMallowsScore(result_dict["precision"], result_dict["recall"])
    result_dict["silhouette score"] = silhouetteScore(clusters, distance_matrix)

    return result_dict


