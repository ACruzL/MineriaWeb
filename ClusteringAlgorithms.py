import numpy as np
from textprocessing import cosine_similarity


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

# list = [[0,1,0,1,1],[1,1,1,0,0],[0,1,1,1,1]]
#
# dist = distance_matrix(list)
# print(dist)

