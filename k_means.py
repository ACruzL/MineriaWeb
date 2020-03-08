# https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/
# https://nlp.stanford.edu/IR-book/html/htmledition/dot-products-1.html#eqn:cosine

import numpy as np
import random
from pprint import pprint
from textprocessing import cosine_similarity, vector_module

def k_means(initial_group, k):
    # make a list of k lists, and every list has its centroid, which is, for the first iteration,
    # one random element of the original group
    samples = random.sample(list(initial_group.items()), k=k)

    k_groups = [[x[0]] for x in samples]

    # print(k_groups)
    last_centroids = None
    centroids = []
    for set_s in k_groups:
        temp_modules = []
        for i in set_s:
            temp_modules.append(vector_module(initial_group[i]))
        centroids.append(np.mean(temp_modules))

    # print(centroids)


    while True:  # simulando un do-while...
        print("iteration")      
        for item in list(initial_group.keys()):
            mod_diff = []
            for group, centroid in zip(k_groups, centroids):
                representer = group[0]
                print(representer, "////", item)
                if not item == representer:
                    vec = initial_group[item]
                    mod_diff.append(abs(vector_module(vec) - centroid))
                    
            min_index = np.argmin(mod_diff)
            k_groups[min_index].append(item)

        last_centroids = centroids
        centroids = []
        pprint(k_groups)
        for set_s in k_groups:
            temp_modules = []
            for i in set_s:
                temp_modules.append(vector_module(initial_group[i]))
            centroids.append(np.mean(temp_modules))

        pprint(centroids)
        print(np.count_nonzero(np.equal(last_centroids, centroids)))
        if np.count_nonzero(np.equal(last_centroids, centroids)) == 0:
            break



    return k_groups
    # recalculate centroid have to think about it

    # start over i guess
