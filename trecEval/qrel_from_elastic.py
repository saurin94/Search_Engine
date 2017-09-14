from elasticsearch import Elasticsearch
from collections import defaultdict, OrderedDict

all_topics = {"152501": "recent immigration order obama",
              "152502": "immigration 20th century",
              "152503": "illegal immigration"}

es = Elasticsearch()


def get_result(query, index_name, type):
    document_set = set()
    try:
        res = None
        try:
            query_final = {
                "query": {
                    "match": {
                        "text": query
                    }},
                "sort": [
                    "_score"
                ],
                'size': 2000

            }
            res = es.search(index=index_name, doc_type=type, _source_include=['docno', 'url'],
                            body=query_final)
        except Exception, e:
            print "Error in query" , e.message

        result_ranked_list = defaultdict(lambda: 0.0)
        q_rel = OrderedDict()
        for hit in res['hits']['hits']:
            if len(document_set) == 1000:
                break
            docno = str(hit['_source']['docno'].encode('utf-8', 'ignore'))
            normal_doc_no = docno.lower()
            if normal_doc_no not in document_set:
                result_ranked_list[docno] = float(hit['_score'])
                document_set.add(normal_doc_no)
        print 'before return'
        return result_ranked_list
    except Exception, e:
        print "Exception : ", e.message


def write_ranked_list(result_dict, topic_id):
    rank = 1
    f = open('result_1000.txt', 'a+')
    for doc_id, score in result_dict.iteritems():
        f.write(str(topic_id) + '<:>Q0<:>' + doc_id + '<:>' + str(rank) + '<:>' + str(score) + '<:>Exp\n')
        rank += 1


def write_q_rel(qrel, topic_id):
    f = open('qrel_crawled_saurin_1000.txt', 'a+')
    for docId, grade in qrel.iteritems():
        f.write(str(topic_id) + '<:>0<:>' + docId + '<:>' + str(grade) + '\n')


if __name__ == '__main__':
    for topic_id in OrderedDict(sorted(all_topics.items())):
        print topic_id
        result = get_result(str(all_topics[topic_id]), 'mi', 'document')
        write_ranked_list(result, topic_id)
