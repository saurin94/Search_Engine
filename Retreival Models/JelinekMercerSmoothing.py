from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch import TransportError
from GetDocWithJelinek import DocIDProviderForJelinek
from RetrievalModels import RetrievalModel


def termmDictFunction(allDoc, finalTerm):
    es = Elasticsearch()
    termDict = {}
    # Get each term
    inlineQuery = "double ttf =_index['text'][\"" + finalTerm + "\"].ttf(); return Math.log10(0.4*(ttf/178097.0))"
    termQuery = {
        "size": 1,
        "_source": "false",
        "query": {
            "term": {
                "text": finalTerm
            }
        },
        "script_fields": {
            "unigramLm": {
                "script": {
                    "lang": "groovy",
                    "inline": inlineQuery
                }
            }
        }
    }
    try:
        res = es.search(index="ap_dataset", doc_type="HW1", body=termQuery,
                        filter_path="hits.hits.fields.unigramLm", scroll="1m")
    except TransportError as e:
        print(e.info)
    total = res
    value = total['hits']['hits'][0]['fields']['unigramLm'][0]
    for docId in allDoc:
        termDict[docId] = value

    return termDict


def matchDictFunction(finalTerm):
    matchDict = {}
    es = Elasticsearch()
    inlineQuery = "double tf = _index['text'][\"" + finalTerm + "\"].tf(); double ttf = _index['text'][\"" + finalTerm + "\"].ttf(); double docLen = _source.text.split().size(); return Math.log10(0.6*(tf/docLen) + 0.4*(ttf/178097.0))"
    termQuery = {
        "size": 10000,
        "_source": "false",
        "query": {
            "match": {
                "text": finalTerm
            }
        },
        "script_fields": {
            "unigramLm": {
                "script": {
                    "lang": "groovy",
                    "inline": inlineQuery
                }
            }
        }
    }
    res = es.search(index="ap_dataset", doc_type="HW1", body=termQuery,
                    filter_path="_scroll_id,hits.total,hits.hits._id,hits.hits.fields.unigramLm", scroll="1m")
    docFreq = res['hits']['total']
    total = res
    if docFreq > 0:
        while (len(total['hits']['hits']) != 0):
            for items in total['hits']['hits']:
                doc_id = items['_id']
                if matchDict.has_key(doc_id):
                    prevValue = matchDict[doc_id]
                    stats = float(items['fields']['unigramLm'][0])
                    matchDict[doc_id.encode('utf-8')] = prevValue + stats
                else:
                    stats = float(items['fields']['unigramLm'][0])
                    matchDict[doc_id.encode('utf-8')] = stats
            sid = total['_scroll_id']
            total = es.scroll(scroll_id=sid, scroll='1m')

    return matchDict


class JelinekMercer(object):
    def __init__(self):
        # Get all queries
        directory = "D:\\IR\\IR_data\\AP_DATA" + "\\" + "query_desc.51-100.short.txt"
        with open(directory, "r") as r:
            allQueries = r.readlines()

        # Establish connection
        es = Elasticsearch()
        q = IndicesClient(es)
        allDocID = DocIDProviderForJelinek()
        allDoc = allDocID.getDocID()
        # Get all queries in ascending order in dictionary
        queryDict = {}
        for each_query in allQueries:
            queryDict[int(each_query.split()[0].replace(".", ""))] = ' '.join(each_query.split()[1:])
        # Iterate through each query.
        for queryNo, query in queryDict.iteritems():
            print ("Into query ----------------")
            queryDict = {}
            query = query.replace("Document", "")
            # Elastic search query for stopwords removal and stemming
            queryResult = q.analyze(index="ap_dataset", analyzer="my_english", text=query)
            # Iterate through each term
            for term in queryResult['tokens']:
                finalTerm = term['token'].encode("utf-8")
                termDict = termmDictFunction(allDoc, finalTerm)
                matchDict = matchDictFunction(finalTerm)

                for docID, value in matchDict.iteritems():
                    if termDict.has_key(docID):
                        termDict[docID] = value
                    else:
                        termDict[docID] = value

                for docID, value in termDict.iteritems():
                    if queryDict.has_key(docID):
                        prev = queryDict[docID]
                        queryDict[docID] = prev + value
                    else:
                        queryDict[docID] = value
                # print queryDict
            r = RetrievalModel()
            r.unigramJM(queryNo, queryDict)

h = JelinekMercer()