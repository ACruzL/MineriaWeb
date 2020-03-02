# TF and IDF implementations taken from: https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/

from nltk.corpus import stopwords 
from nltk.tokenize import RegexpTokenizer
from math import log

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

def text_preprocessing(documents):
    '''Función para calcular el vector de cada palabra en el contexto de su documento, y 
    el conjunto de todos los documentos a analizar.'''
    vector_dict = dict()
    for doc in documents:
        print(doc)
        tokens = regex_tokenizer.tokenize(doc.lower())
        aux_list = []
        for token in tokens:
            if not token in stopwords:
                print(token)
                tf = term_frequency(token, doc)
                idf = inverse_document_frequency(token, allDocuments)
                tf_idf = tf * idf
                print("\tTF:", tf)
                print("\tIDF:", idf)
                print("\tTF * IDF:", tf_idf)
                if not token in aux_list:
                    aux_list.append((token, tf_idf))

        vector_dict[doc] = set(aux_list)

        print("\n____________________\n")

    print(vector_dict)
    return vector_dict
