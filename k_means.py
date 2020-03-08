import numpy as np
import random
from textprocessing import cosine_similarity

def k_means(initial_group, k):
    # make a list of k lists, and every list has its centroid, which is, for the first iteration,
    # one random element of the original group
    aux_groups = random.sample(list(initial_group.keys()), k=k)

    k_groups = []
    for i in aux_groups:
        k_groups.append([(i, initial_group[i])])
        del initial_group[i]

    # iterate through the whole initial group and compare to every centroid, 
    # assign it where it fits most (min cosine similarity means minimum distance)
    while len(initial_group) > 0:
        for item in list(initial_group.items()):
            cosine_array = []
            for centroid in k_groups:
                    cosine_array.append(cosine_similarity(item[1], centroid[0][1]))
                    
            min_index = np.argmin(cosine_array)
            k_groups[min_index].append(item)
        
            del initial_group[item[0]]


    return k_groups
    # recalculate centroid have to think about it

    # start over i guess
