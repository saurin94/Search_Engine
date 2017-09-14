from elasticsearch import Elasticsearch


class DocIDProvider(object):
    def getDoc(self):
        es = Elasticsearch()
        query = {
            "size": 10000,
            "_source": "false",
            "query": {
                "match_all": {}
            },
            "stored_fields": [
                "_id"
            ],
            "script_fields": {
                "defaultValue": {
                    "script": {
                        "lang": "groovy",
                        "inline": "int docLen = _source.text.split().size();return Math.log(1/(docLen + 178097))"
                    }
                }
            }
        }
        res = es.search(index="ap_dataset", doc_type="HW1", body=query, scroll="1m",
                        filter_path="hits.total,_scroll_id,hits.hits._id,hits.hits.fields.defaultValue")
        docFreq = res['hits']['total']
        total = res
        # print type(total['hits']['hits'][0]['_id'].encode("utf-8"))
        # print len(total['hits']['hits'])
        allDoc = {}
        docFreq = res['hits']['total']
        total = res
        if docFreq > 0:
            while (len(total['hits']['hits']) > 0):
                for docs in total['hits']['hits']:
                    docID = docs['_id'].encode("utf-8")
                    default = docs['fields']['defaultValue'][0]
                    allDoc[docID] = default
                sid = total['_scroll_id']
                # print(" preparing for scroll ")
                total = es.scroll(scroll_id=sid, scroll='1m')
        #print allDoc
        return allDoc


h = DocIDProvider()
h.getDoc()
