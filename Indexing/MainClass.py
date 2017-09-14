import Indexing
import ReadFromFilesToJson
import MergerCompleteFast
import OkapiQuery
import tfIdfQuery
import bm25query
import unigramLaplaceQuery
import ProximityQuery
class Main(object):

    def __init__(self):

        #Get all docId , Text to Json file
        fileToJson = ReadFromFilesToJson.WriteDataToJson()
        # -------------------------------------------------------------------------------------#

        #Tokenize and Index : From Json to 365 - Catalog and 365- Indexes
        tokenizeAndIndex = Indexing.Indexing.indexingAsIs()
        # -------------------------------------------------------------------------------------#

        #Merging 365 Catalogs and 365 Indexes
        merger = MergerCompleteFast.MergingIndexes()
        # -------------------------------------------------------------------------------------#

        #------------------------------ Retrieval Models --------------------------------------#
        #Okapi
        okapi = OkapiQuery.OkapiQuery()
        # -------------------------------------------------------------------------------------#
        #tfidf
        tfidf = tfIdfQuery.tfIdfQuery()
        # -------------------------------------------------------------------------------------#
        #bm25
        bm25 = bm25query.bm25Query()
        # -------------------------------------------------------------------------------------#
        #unigramLaplace
        laplace = unigramLaplaceQuery.unigramLaplaceQuery()
        # -------------------------------------------------------------------------------------#
        #proximity
        proximity = ProximityQuery.ProximityQuery()

        # ---------------------------- End Retrieval Models -----------------------------------#
        # -------------------------------------------------------------------------------------#

main = Main()
