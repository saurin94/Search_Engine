from Bm25Query import BM25Query
from JelinekMercerSmoothing import JelinekMercer
from OkapiQuery import OkapiQuery
from tfIdfQuery import tfIDFQuery
from unigramLaplace import LaplaceSmoothing

class RetreivalModelsComplete(object):
    def __init__(self):
        okapi = OkapiQuery()
        print("-------------Okapi done---------------")
        tfidf = tfIDFQuery()
        print("-------------tf-idf done---------------")
        bm25 = BM25Query()
        print("-------------bm25 done---------------")
        unigramLaplace = LaplaceSmoothing()
        print("-------------laplace done---------------")
        jelinek = JelinekMercer()
        print("------------jelinek done---------------")

run = RetreivalModelsComplete()
