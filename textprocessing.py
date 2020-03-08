# TF and IDF implementations taken from: https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/

from nltk.corpus import stopwords 
from nltk.tokenize import RegexpTokenizer
from math import log, pow, sqrt

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
    vec_sum = 0
    for value1, value2 in zip(vec1, vec2):
        vec_sum += value1[1] * value2[1]

    return vec_sum

def vector_module(vec1):
    square_sum = 0
    for value in vec1:
        square_sum += pow(value[1], 2)

    return sqrt(square_sum)

def cosine_similarity(vec1, vec2):
    dot_prod = dot_product(vec1, vec2)
    mod1 = vector_module(vec1)
    mod2 = vector_module(vec2)

    return dot_prod / (mod1 * mod2)

    
def word2vec(documents):
    '''Función para calcular el vector de cada palabra en el contexto de su documento, y 
    el conjunto de todos los documentos a analizar.'''
    vector_dict = dict()
    for doc in documents:
        tokens = regex_tokenizer.tokenize(doc)
        aux_list = []
        for token in tokens:
            if not token.lower() in stopwords:
                tf = term_frequency(token, doc)
                idf = inverse_document_frequency(token, documents)
                tf_idf = tf * idf
                
                aux_list.append((token, tf_idf))

        vector_dict[doc] = set(aux_list)

    return vector_dict
