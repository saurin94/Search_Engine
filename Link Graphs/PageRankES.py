import elasticsearch
from elasticsearch import TransportError
out_link_map = {}
f = open("out_link_merged_new.txt", "w")


def fetch_outlink():
    global out_link_map
    es = elasticsearch.Elasticsearch()
    try:
        query = {
            "size": 10000
        }
        res = es.search(index="mi", doc_type="document",
                        _source_include=["url", "out_links"], scroll="1m", body=query, request_timeout=70)
    except TransportError as e:
        print(e.info)
    docFreq = res['hits']['total']
    total = res
    count = 1
    if docFreq > 0:
        while len(total['hits']['hits']) != 0:
            for items in total['hits']['hits']:
                count += 1
                out_links = items['_source']['out_links']
                url = items['_source']['url'].encode("utf-8", "ignore").strip("\n").strip("\t")
                f.write(url + " " + " ".join(out_links).encode("utf-8", "ignore") + "\n")
            sid = total['_scroll_id']
            print "Scrolling"
            print "Count : ", count
            try:
                total = es.scroll(scroll_id=sid, scroll='1m', request_timeout=70)
            except Exception, e:
                print "Scroll Error : ", e.message


fetch_outlink()
f.close()