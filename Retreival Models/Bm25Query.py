from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch import TransportError
from RetrievalModels import RetrievalModel

class BM25Query(object):
    def __init__(self):
        # Get all queries
        directory = "D:\\IR\\IR_data\\AP_DATA" + "\\" + "query_desc.51-100.short.txt"
        with open(directory, "r") as r:
            allQueries = r.readlines()

        # Establish connection
        es = Elasticsearch()
        q = IndicesClient(es)

        # Get all queries in ascending order in dictionary
        queryDict = {}
        for each_query in allQueries:
            queryDict[int(each_query.split()[0].replace(".",""))] = ' '.join(each_query.split()[1:])

        # Iterate through each query.
        for queryNo, query in queryDict.iteritems():
            docDict = {}
            query = query.replace("Document", "")
            # Elastic search query for stopwords removal and stemming
            queryResult = q.analyze(index="ap_dataset", analyzer="my_english", text=query)
            # Iterate through each term
            print (" ------------ into query -----------------")
            for term in queryResult['tokens']:
                # Get each term
                finalTerm = term['token'].encode("utf-8")
                termFreqInQuery = 0
                for term in queryResult['tokens']:
                    if finalTerm == term['token'].encode("utf-8"):
                        termFreqInQuery += 1
                factor = float((termFreqInQuery + 100.0*termFreqInQuery)/(termFreqInQuery + 100.0))
                inlineQuery = "double tf =_index['text']" + "[\"" + finalTerm + "\"].tf(); double df =_index['text'] " + "[\"" + finalTerm + "\"].df(); double ttf = _index['text']" + "[\"" + finalTerm + "\"].ttf(); double docLen = _source.text.split().size(); double logValue = Math.log10(84678.50/(df+0.50));double factor =" + str(factor) + ";double mainNum = tf + 1.20*tf;double mainDen = tf + 1.20*((0.25 + 0.25*(docLen/441.5)));double main = mainNum/mainDen;return logValue*factor*main"
                termQuery = {
                    "size": 5000,
                    "_source": "false",
                    "query": {
                        "term": {
                            "text": finalTerm
                        }
                    },
                    "script_fields": {
                        "bm25Score": {
                            "script": {
                                "lang": "groovy",
                                "inline": inlineQuery
                            }
                        }
                    }
                }
                try:
                    res = es.search(index="ap_dataset", doc_type="HW1", body=termQuery, filter_path="_scroll_id,hits.hits._id,hits.hits.fields.bm25Score,hits.total",scroll="1m")
                except TransportError as e:
                    print(e.info)
                docFreq = res['hits']['total']
                total = res
                if docFreq > 0:
                    while (len(total['hits']['hits'])!=0):
                        for items in total['hits']['hits']:
                            doc_id = items['_id']
                            if docDict.has_key(doc_id):
                                prevValue = docDict[doc_id]
                                stats = float(items['fields']['bm25Score'][0])
                                docDict[doc_id.encode('utf-8')] = prevValue + stats
                            else:
                                stats = float(items['fields']['bm25Score'][0])
                                docDict[doc_id.encode('utf-8')] = stats
                        sid = total['_scroll_id']
                        # print(" preparing for scroll ")
                        total = es.scroll(scroll_id=sid, scroll='1m')

            r = RetrievalModel()
            r.bm25calculate(queryNo,docDict)

BM25Query()