from collections import defaultdict, OrderedDict

# -----------------------------------------------#

f = open('qrel_crawled_saurin_500.txt', 'r')
saurin_dict = defaultdict(lambda: OrderedDict())
data = f.readlines()
f.close()
for line in data:
    data_final = line.split('<:>')
    search_query = int(data_final[0])
    dummy = data_final[1]
    doc_id = data_final[2]
    score = int(data_final[3])
    saurin_dict[search_query][doc_id] = score
# -----------------------------------------------#

f = open('qrel_crawled_sushant_500.txt', 'r')
sushant_dict = defaultdict(lambda: OrderedDict())
data = f.readlines()

f.close()
for line in data:
    data_final = line.split('<:>')
    search_query = int(data_final[0])
    dummy = data_final[1]
    doc_id = data_final[2]
    score = int(data_final[3])
    sushant_dict[search_query][doc_id] = score
# -----------------------------------------------#

f = open('qrel_crawled.txt', 'r')
koosh_dict = defaultdict(lambda: OrderedDict())
data = f.readlines()

f.close()
for line in data:
    data_final = line.split('<:>')
    search_query = int(data_final[0])
    dummy = data_final[1]
    doc_id = data_final[2]
    score = int(data_final[3])
    koosh_dict[search_query][doc_id] = score

# -------------------------------------------------#
f = open('final_qrel.txt', 'a+')
final_score = 0
for search_query, inner_dict in saurin_dict.iteritems():
    doc_set = set()
    for doc_id, score in inner_dict.iteritems():
        saurin_score = score
        if len(doc_set) == 200:
            break
        if doc_id in koosh_dict[search_query] and doc_id in sushant_dict[search_query]:

            sushant_score = sushant_dict[search_query][doc_id]
            koosh_score = koosh_dict[search_query][doc_id]
            if sushant_score == koosh_score or sushant_score == saurin_score:
                final_score = sushant_score
            elif koosh_score == sushant_score or koosh_score == saurin_score:
                final_score = koosh_score
            elif saurin_score == sushant_score or saurin_score or koosh_score:
                final_score = saurin_score
            else:
                final_score = int((saurin_score + koosh_score + sushant_score)/3)
            doc_set.add(doc_id)
            f.write(str(search_query) + "()" + str(0) + "()" + str(doc_id) + "()" + str(final_score) + '()' + str('EVAL') + "\n")

f.close()