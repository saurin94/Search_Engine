from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch import TransportError
from RetrievalModels import RetrievalModel
from GetDocID import DocIDProvider
import math


class LaplaceSmoothing(object):
    def __init__(self):
        # Get all queries
        directory = "D:\\IR\\IR_data\\AP_DATA" + "\\" + "query_desc.51-100.short.txt"
        with open(directory, "r") as r:
            allQueries = r.readlines()
        # Establish connection
        es = Elasticsearch()
        q = IndicesClient(es)
        allDoc = DocIDProvider()
        allDocFinal = allDoc.getDoc()
        # Get all queries in ascending order in dictionary
        queryDict = {}
        for each_query in allQueries:
            queryDict[int(each_query.split()[0].replace(".", ""))] = ' '.join(each_query.split()[1:])

        # Iterate through each query.
        for queryNo, query in queryDict.iteritems():
            docDict = {}
            query = query.replace("Document", "")
            query = query.replace("report", "")

            # Elastic search query for stopwords removal and stemming
            queryResult = q.analyze(index="ap_dataset", analyzer="my_english", text=query)
            totalTermInQuery = len(queryResult['tokens'])

            for docId, default in allDocFinal.iteritems():
                docDict[docId] = totalTermInQuery*default
            # Iterate through each term
            print (" ------------ into query -----------------")
            for term in queryResult['tokens']:
                # Get each term
                finalTerm = term['token'].encode("utf-8")
                inlineQuery = "double tf =_index['text']" + "[\"" + finalTerm + "\"].tf(); double docLen = _source.text.split().size();double plaplace = (tf + 1.0)/(docLen + 178097.0); return Math.log10(plaplace)"
                termQuery = {
                    "size": 10000,
                    "_source": "false",
                    "query": {
                        "match": {
                            "text": finalTerm
                        }
                    },
                    "script_fields": {
                        "plaplace": {
                            "script": {
                                "lang": "groovy",
                                "inline": inlineQuery
                            }
                        }
                    }
                }
                try:
                    res = es.search(index="ap_dataset", doc_type="HW1", body=termQuery,
                                    filter_path="_scroll_id,hits.hits._id,hits.hits.fields.plaplace,hits.total",
                                    scroll="1m")
                except TransportError as e:
                    print(e.info)
                docFreq = res['hits']['total']
                total = res
                if docFreq > 0:
                    while len(total['hits']['hits']) != 0:
                        for items in total['hits']['hits']:
                            doc_id = items['_id']
                            if docDict.has_key(doc_id):
                                prevValue = docDict[doc_id]
                                stats = float(items['fields']['plaplace'][0]) - math.log10(1.0/178097.0)
                                docDict[doc_id.encode('utf-8')] = prevValue + stats
                            # else:
                            #     stats = float(items['fields']['plaplace'][0]) - math.log(1.0/178097.0)
                            #     docDict[doc_id.encode('utf-8')] = stats
                        sid = total['_scroll_id']
                        total = es.scroll(scroll_id=sid, scroll='1m')

            r = RetrievalModel()
            r.laplaceSmoothing(queryNo, docDict)
LaplaceSmoothing()

