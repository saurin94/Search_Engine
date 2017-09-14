import json

import elasticsearch
es = elasticsearch.Elasticsearch()
outlinkDict = {}
inlinkDict = {}


def outlink_map():
    global outlinkDict
    count = 1
    f = open("out_link_merged.txt", "r")
    for outlinks_data in f.readlines():
        outlinks_list_maker = outlinks_data.split()
        try:
            outlink_key = outlinks_list_maker[0]
        except Exception, e:
            count += 1
            pass
        if len(outlinks_data) > 0:
            outlink_value = set(outlinks_list_maker[1:])
        else:
            outlink_value = set([])
        if outlink_key in outlinkDict:
            prev = outlinkDict[outlink_key]
            prev.update(outlink_value)
            outlinkDict[outlink_key] = prev
        else:
            outlinkDict[outlink_key] = outlink_value
    print "Outlink Dict Length : ", len(outlinkDict)
    print "Count : ", count


def outlink_to_inlink():
    global outlinkDict
    global inlinkDict
    for outlink_key, outlink_value in outlinkDict.iteritems():
        for link in outlink_value:
            if link in inlinkDict:
                prev = inlinkDict[link]
                prev.update([outlink_key])
                inlinkDict[link] = prev
            else:
                inlinkDict[link] = set([outlink_key])
    print "Inlink Dict Length : ", len(inlinkDict)


def write_inlink():
    f = open("linkgraph_queried.txt", "w")
    for key, value in inlinkDict.iteritems():
        f.write(key + " " + " ".join(value) + "\n")
    f.close()


def get_base_docs():
    global es
    query = {
        "query": {
            "match": {
                "text": "illegal immigration"
            }
        },
        "size": 1000
    }
    res = es.search(index="mi", doc_type="document", body=query, request_timeout=70)
    f = open("BaseURLdocs.json", "w+")
    json.dump(res, f, indent=1)
    f.close()


def get_base_details():
    base_url_set = set()
    f = open("BaseURLdocs.json", "r")
    data = json.load(f)
    f.close()
    info = data['hits']['hits']
    count = 1
    for i in info:
        url = i['_source']['url'].rstrip("/")
        base_url_set.add(url)
        count += 1
    f = open("baseSetUrls", "w")
    for each_url in base_url_set:
        f.write(each_url.encode("utf-8", "ignore"))
        f.write("\n")
    f.close()


get_base_details()

# outlink_map()
# outlink_to_inlink()
# write_inlink()
# get_base_docs()

