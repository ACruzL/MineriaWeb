# https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/
# https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html#eqn:cosine

import numpy as np
import random
from pprint import pprint
from textprocessing import cosine_similarity
import copy

def k_means(sparse_matrix, k):

    # take k random rows from sparse_matrix
    init_centroids = random.sample(list(np.arange(0, len(sparse_matrix), dtype=np.uint8)), k=k)
    k_centroids = [[x] for x in init_centroids]
    print(k_centroids)
    last_round = copy.deepcopy(k_centroids)

    while True:
        print("iteration")
        calculate_distances(k_centroids, sparse_matrix)     

        last_round_vecs = get_vectors_from_indices(last_round, sparse_matrix)
        k_centroids_vecs = get_vectors_from_indices(k_centroids, sparse_matrix)

        last_round_means = calculate_nearest_to_mean(last_round_vecs, sparse_matrix)
        mean_group_vectors = calculate_nearest_to_mean(k_centroids_vecs, sparse_matrix)

        stop_condition = np.count_nonzero(np.equal(last_round_means, mean_group_vectors))
        print(stop_condition)
        
        if stop_condition == k:
            return k_centroids
        else:
            last_round = copy.deepcopy(k_centroids)
            k_centroids.clear()
            k_centroids = copy.deepcopy([[x] for x in mean_group_vectors])



            

def get_vectors_from_indices(index_arr, sparse_matrix):
    vector_array = []
    for group in index_arr:
        aux = []
        for index in group:
            aux.append(sparse_matrix[index])

        vector_array.append(aux)

    return vector_array


def calculate_nearest_to_mean(centroids, sparse_matrix):
    nearest_index = []
    for group in centroids:
        mean_group = np.mean(group, axis=0)
        cosine_list = []
        for i in range(len(sparse_matrix)):
            cosine_list.append(1 - cosine_similarity(sparse_matrix[i], mean_group))

        min_index = np.argmin(cosine_list)
        nearest_index.append(min_index)
    
    return nearest_index
    

def calculate_distances(centroids, sparse_matrix):
    for i in range(len(sparse_matrix)):
        cosine_list = []
        for c in range(len(centroids)):
            cosine_list.append(1 - cosine_similarity(sparse_matrix[i], sparse_matrix[c]))

        min_index = np.argmin(cosine_list)
        centroids[min_index].append(i)
