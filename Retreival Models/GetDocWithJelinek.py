from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch import TransportError


class DocIDProviderForJelinek(object):
    def getDocID(self):
        es = Elasticsearch()
        query = {
            "size": 10000,
            "_source": "false",
            "query": {
                "match_all": {}
            },
            "stored_fields": [
                "_id"
            ]
        }
        res = es.search(index="ap_dataset", doc_type="HW1", body=query, scroll="1m",
                        filter_path="hits.total,_scroll_id,hits.hits._id")
        allDoc = []
        docFreq = res['hits']['total']
        total = res
        if docFreq > 0:
            while (len(total['hits']['hits']) > 0):
                for docs in total['hits']['hits']:
                    docID = docs['_id'].encode("utf-8")
                    allDoc.append(docID)
                sid = total['_scroll_id']
                # print(" preparing for scroll ")
                total = es.scroll(scroll_id=sid, scroll='1m')
        return allDoc

h = DocIDProviderForJelinek()
h.getDocID()
