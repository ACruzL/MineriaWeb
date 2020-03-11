# TF and IDF implementations taken from: https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/

from nltk.corpus import stopwords 
from nltk.tokenize import RegexpTokenizer
from math import log, pow, sqrt
import numpy as np

regex = "\w+\'\w+|\w+"
regex_tokenizer = RegexpTokenizer(regex)

stopwords = set(stopwords.words('english'))

def term_frequency(term, document):
    normalizeDocument = document.lower().split()
    return normalizeDocument.count(term.lower()) / float(len(normalizeDocument))

def inverse_document_frequency(term, allDocuments):
    numDocumentsWithThisTerm = 0
    for doc in allDocuments:
        if term.lower() in doc.lower().split():
            numDocumentsWithThisTerm = numDocumentsWithThisTerm + 1
 
    if numDocumentsWithThisTerm > 0:
        return 1.0 + log(float(len(allDocuments)) / numDocumentsWithThisTerm)
    else:
        return 1.0

def dot_product(vec1, vec2):
    return np.sum(np.array(vec1) * np.array(vec2))

def vector_module(vec1):
    square_sum = 0
    for value in vec1:
        square_sum += pow(value, 2)

    return sqrt(square_sum)

def cosine_similarity(vec1, vec2):
    dot_prod = dot_product(vec1, vec2)
    mod1 = vector_module(vec1)
    mod2 = vector_module(vec2)

    return dot_prod / (mod1 * mod2)

    
import scipy.sparse as sp

def word2vec(documents):
    '''Función para calcular el vector de cada palabra en el contexto de su documento, y 
    el conjunto de todos los documentos a analizar.'''
    dictionary = dict()
    document_list = []
    index = 0
    for doc in documents:
        aux_list = []
        tokens = regex_tokenizer.tokenize(doc.lower())
        for token in tokens:
            if token not in stopwords:
                if token not in dictionary:
                    dictionary[token] = index
                    aux_list.append(index)
                    index += 1
                else:
                    aux_list.append(dictionary[token])

        document_list.append(aux_list)

    sparse_matrix = sp.lil_matrix((len(documents),len(dictionary)), dtype=int)
    for row_index, col_indices in enumerate(document_list):
        sparse_matrix[row_index, col_indices] = 1

    sparse_matrix = sparse_matrix.toarray()

    return sparse_matrix

list = ["hola me llamo alex","aa patata hola"]

sparse_matrix = word2vec(list)

print(cosine_similarity(sparse_matrix[0],sparse_matrix[1]))
