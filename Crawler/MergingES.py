import json

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch import TransportError
es = Elasticsearch()
count = 0
update_merge_count = 1
update_index_count = 1


class Merging(object):
    def __init__(self):
        global es
        global count
        visited = set()
        limit = 500
        i = 1
        try:
            f = open("Try20k.json", "r")

            for line in f:
                if i <= limit:
                    count += 1
                    try:
                        jsonNode = json.loads(line)
                        # normlURL = Get url as it is
                        normURL = str(jsonNode['docno'].encode("utf-8", "ignore"))
                        # finalNormUrl = lowercase normUrl
                        if normURL[-1] == "/":
                            normURL = normURL[:-1]
                        finalNormUrl = normURL.lower()
                        # Check finalNormURL is in visited
                        if finalNormUrl not in visited:
                            self.update("demo", "document", normURL, line)
                            visited.add(finalNormUrl)
                    except Exception, e:
                        print "Cant load json for current line ,Error :", e
                i += 1
                print "Merge Count : ", update_merge_count
                print "Index Count : ", update_index_count
        except Exception, e:
            print "File Open Error :", e
        finally:
            es = None
            print "Count :", str(count)
            print "Visited URLs :", len(visited)

    def update(self, indexName, type, docno, json):
        global update_merge_count
        global update_index_count
        global es
        try:
            res = None
            try:
                res = es.get(index=indexName, doc_type=type, id=docno, _source_include=['docno', 'author'])
            except Exception, e:
                print "Result Error Top: ", e.message
            if res is not None and res['found']:
                print "\nTrying to merge docno :", docno
                oldauthor = str(res['_source']['author'])
                newauthor = oldauthor + " Saurin"

                bodyQuery = "ctx._source.author = \"" + newauthor + "\""
                finalQuery = {"script": {"lang": "painless", "inline": bodyQuery}}
                try:
                    updateRes = es.update(index=indexName, doc_type=type, id=docno, body=finalQuery)

                    if updateRes['result'] == "updated":
                        print "Merged Successfully | doc no :", docno
                        update_merge_count += 1
                    else:
                        print "Not Merged | doc no :", docno
                except Exception, e:
                    print "Update Error : ", e
            else:
                print "Trying to insert ! doc no :", docno
                try:
                    res = es.index(index=indexName, doc_type=type, id=docno, body=json)
                    if res['created']:
                        print "Indexed Successfully | doc no :", docno
                        update_index_count += 1
                    else:
                        print "Not Indexed | doc no :", docno
                except Exception, e:
                    print "Indexing failed | doc no:", docno
        except Exception, e:
            print "Response Error : ", e.message


Merging()





