import numpy as np
from textprocessing import cosine_similarity
import random
from pprint import pprint
import copy
from sklearn.preprocessing import normalize

#                    ########## ALGORITMO BDSCAN ###########
def bdscan(sparse_matrix, eps= 0.75 , minPts= 2):
    clusters = []
    visited = np.zeros(len(sparse_matrix))
    noise_pts = set()
    type = np.zeros(len(sparse_matrix))
    dist_matrix = distance_matrix(sparse_matrix)
    for x in range(len(sparse_matrix)):
        if visited[x] == 0:
            visited[x] = 1
            neighborPts = regionQuery(x, dist_matrix, eps)
            if len(neighborPts) < minPts:
                noise_pts.add(x)
            else:
                clusters.append(expandCluster(x, neighborPts, eps, minPts, visited, noise_pts, dist_matrix))

    return clusters, noise_pts


def expandCluster(P, neighborPts, eps, minPts, visited, noise_pts, dist_matrix):
    cluster = [P]
    for x in neighborPts:
        if visited[x] == 1 and x in noise_pts:
            noise_pts.remove(x)
            cluster.append(x)
        elif visited[x] == 0:
            visited[x] = 1
            neighborPts = regionQuery(x, dist_matrix, eps)
            if len(neighborPts) >= minPts:
                cluster += (expandCluster(x, neighborPts, eps, minPts, visited, noise_pts, dist_matrix))
            else:
                cluster.append(x)
    return cluster

def regionQuery(P, dist_matrix, eps):
    return np.where(dist_matrix[P] < eps)[0]

def distance_matrix(sparse_matrix):
    rows = len(sparse_matrix)
    dist_matrix = np.zeros((rows, rows))
    for i in range(rows):
        print("Row: {}".format(i))
        for j in range(i+1, rows):
            dist_matrix[i][j] = 1 - cosine_similarity(sparse_matrix[i], sparse_matrix[j])
            dist_matrix[j][i] = dist_matrix[i][j]

    return np.array(dist_matrix)






#                    ########## ALGORITMO K MEANS ###########
# https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/
# https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html#eqn:cosine

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
            if not np.array_equal(sparse_matrix[i], sparse_matrix[c]):
                cosine_list.append(1 - cosine_similarity(sparse_matrix[i], sparse_matrix[c]))

        min_index = np.argmin(cosine_list)
        centroids[min_index].append(i)









#                    ########## ALGORITMO K MEANS ++ ###########
def k_means_plus_plus(sparse_matrix, k):
    # elegir un primer punto aleatorio
    init_centroids = [random.choice(list(np.arange(0, len(sparse_matrix), dtype=np.uint8)))]

    for i in range(k-1):
        # calcular dsitancia de cada punto x respecto a dicho centroide
        distance_to_centroids = calculate_distances_plus_plus(init_centroids, sparse_matrix)

        # normalizar vector de distancias y pasarlo a RANDOM.CHOICE para elegir nuevo centroide
        index_list = [d[0] for d in distance_to_centroids]
        weight_list = [d[1]**2 for d in distance_to_centroids]
        weight_list = [float(x)/max(weight_list) for x in weight_list]

        next_centroid = random.choices(index_list, weights=weight_list, k=1)[0]
        init_centroids.append(next_centroid)

    # take k random rows from sparse_matrix
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

def calculate_distances_plus_plus(centroids, sparse_matrix):
    cosine_list = []
    for i in range(len(sparse_matrix)):
        aux = []
        for c in range(len(centroids)):
            if not np.array_equal(sparse_matrix[i], sparse_matrix[c]):
                aux.append(1 - cosine_similarity(sparse_matrix[i], sparse_matrix[c]))
    
        if len(aux) > 0:
            min_index = np.argmin(aux)
            cosine_list.append((i, aux[min_index]))

    return cosine_list












