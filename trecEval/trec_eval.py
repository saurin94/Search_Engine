import sys
from collections import defaultdict
import re
import matplotlib.pyplot as plt
import math

LIMIT = 500

ARGS = sys.argv

if len(ARGS) < 3:
    print \
        """
        trec_eval commandline error.
        Use this way
        >>> python trec_eval.py <-q> <-g> <qrel_file> <test_file>
        Add '-q' options if output is required
        """
    sys.exit(-1)
if ARGS[1] == '-q':
    qrel_file = ARGS[2]
    trec_file = ARGS[3]
else:
    qrel_file = ARGS[1]
    trec_file = ARGS[2]
print \
    """
    Using QREL file as {0}
    Using TREC file as {1}
    """.format(qrel_file, trec_file)

qrel = defaultdict(lambda: {})
num_rel = defaultdict(lambda: 0)
trec = defaultdict(lambda: [])

QREL = open(qrel_file, 'r')
data = QREL.readlines()
for line in data:
    try:
        # topic, dummy, doc_id, rel = re.compile(r"\s+").split('()')
        final = line.split('()')
        print final
        topic = final[0]
        dummy = final[1]
        doc_id = final[2]
        rel = final[3]
        qrel[topic][doc_id] = int(rel)
        num_rel[topic] += int(rel)
    except Exception, e:
        print "QREL_FILE read error : ", e.message

# ------------------------------------------------------------------------#

TREC = open(trec_file, 'r')
for line in TREC:
    final = line.split('()')
    # topic, dummy, doc_id, rank, score, dummy = re.compile(r"\s+").split('<:>')
    topic = final[0]
    dummy = final[1]
    doc_id = final[2]
    rank = final[3]
    score = final[4]
    dummy = final[5]
    trec[topic].append((doc_id, float(score)))
TREC.close()

# ------------------------------------------------------------------------#

cutoffs = [5, 10, 15, 20, 30, 100, 200, 500, 100]
recalls = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
num_topics = 0

# ------------------------------------------------------------------------#

tot_num_ret = 0.0
tot_num_rel = 0.0
tot_num_rel_ret = 0.0
sum_avg_prec = 0.0
sum_r_prec = 0.0
sum_dcg = 0.0
sum_prec_at_cutoffs = [1] * len(cutoffs)
sum_recall_at_cutoffs = [1] * len(recalls)
sum_prec_at_recalls = [1] * len(recalls)
sum_f1_at_cutoffs = [1] * len(cutoffs)
avg_prec_at_cutoffs = [1] * len(cutoffs)
avg_prec_at_recalls = [1] * len(recalls)
avg_recall_at_cutoffs = [1] * len(recalls)
avg_f1_at_cutoffs = [1] * len(cutoffs)

# ------------------------------------------------------------------------#


def plot_graph(avg_prec_at_recalls, qid):
    recall_array = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    plt.plot(recall_array, avg_prec_at_recalls)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.grid(True)
    plt.title('Interpolated Recall - Precision Averages')
    name = "prec_recall_plot_qid_" + str(qid)
    plt.savefig(".//graphs//%s.png" % name)
    plt.close()


def eval_print(qid, ret, rel, rel_ret, avg_prec_at_recalls, mean_avg_prec, avg_prec_at_cutoffs, avg_r_prec ,
               avg_f1_at_cutoffs, avg_recall_at_cutoffs, avg_ndcg):
    plot_graph(avg_prec_at_recalls, qid)
    print "\nQueryid (Num):   ",qid
    print "\n"
    print "Total number of documents over all queries\n"
    print "    Retrieved:    %5d\n" % ret
    print "    Relevant:     %5d\n" % rel
    print "    Rel_ret:      %5d\n" % rel_ret
    print "Interpolated Recall - Precision Averages:\n"
    print "    at 0.00       %.4f\n" % avg_prec_at_recalls[0]
    print "    at 0.10       %.4f\n" % avg_prec_at_recalls[1]
    print "    at 0.20       %.4f\n" % avg_prec_at_recalls[2]
    print "    at 0.30       %.4f\n" % avg_prec_at_recalls[3]
    print "    at 0.40       %.4f\n" % avg_prec_at_recalls[4]
    print "    at 0.50       %.4f\n" % avg_prec_at_recalls[5]
    print "    at 0.60       %.4f\n" % avg_prec_at_recalls[6]
    print "    at 0.70       %.4f\n" % avg_prec_at_recalls[7]
    print "    at 0.80       %.4f\n" % avg_prec_at_recalls[8]
    print "    at 0.90       %.4f\n" % avg_prec_at_recalls[9]
    print "    at 1.00       %.4f\n" % avg_prec_at_recalls[10]
    print "Average precision (non-interpolated) for all rel docs(averaged over queries)\n"
    print "                  %.4f\n" % mean_avg_prec
    print "                  Precision     Recall      F1-Measure\n"
    print "  At    5 docs:   %.4f       %4f      %4f\n" % (avg_prec_at_cutoffs[0], avg_recall_at_cutoffs[0], avg_f1_at_cutoffs[0])
    print "  At   10 docs:   %.4f       %4f      %4f\n" % (avg_prec_at_cutoffs[1], avg_recall_at_cutoffs[1], avg_f1_at_cutoffs[1])
    print "  At   15 docs:   %.4f       %4f      %4f\n" % (avg_prec_at_cutoffs[2], avg_recall_at_cutoffs[2], avg_f1_at_cutoffs[2])
    print "  At   20 docs:   %.4f       %4f      %4f\n" % (avg_prec_at_cutoffs[3], avg_recall_at_cutoffs[3], avg_f1_at_cutoffs[3])
    print "  At   30 docs:   %.4f       %4f      %4f\n" % (avg_prec_at_cutoffs[4], avg_recall_at_cutoffs[4], avg_f1_at_cutoffs[4])
    print "  At  100 docs:   %.4f       %4f      %4f\n" % (avg_prec_at_cutoffs[5], avg_recall_at_cutoffs[5], avg_f1_at_cutoffs[5])
    print "  At  200 docs:   %.4f       %4f      %4f\n" % (avg_prec_at_cutoffs[6], avg_recall_at_cutoffs[6], avg_f1_at_cutoffs[6])
    print "  At  500 docs:   %.4f       %4f      %4f\n" % (avg_prec_at_cutoffs[7], avg_recall_at_cutoffs[7], avg_f1_at_cutoffs[7])
    print "  At 1000 docs:   %.4f       %4f      %4f\n" % (avg_prec_at_cutoffs[8], avg_recall_at_cutoffs[8], avg_f1_at_cutoffs[8])
    print "R-Precision (precision after R (= num_rel for a query) docs retrieved):\n"
    print "    Exact:        %.4f\n" % avg_r_prec
    print "nDCG value for all the relevant documents at k = 5, 10, 20, 50, 100, 200, 300, 500, 1000:"
    print "                  %0.4f" % avg_ndcg


# ------------------------------------------------------------------------#


def calculate_dcg(dcg_list):
    nDCG = 2 ** dcg_list[0] - 1
    for j in range(1, len(dcg_list)):
        nDCG += (2 ** dcg_list[j] - 1) / math.log(j + 1)
    return nDCG


def calculate_f1(a, b):
    if not b or not a:
        return 0.0
    else:
        numerator = 2 * a * b
        denominator = a + b
        return float(numerator/denominator)


for topic in sorted(trec):
    if not num_rel[topic]:
        continue
    num_topics += 1
    href = trec[topic]

    prec_list = {}
    rec_list = {}
    f1 = {}

    num_ret = 0.0
    num_rel_ret = 0.0
    sum_prec = 0.0

    recall_axis = []
    precision_axis = []
    grades_given = []

    for doc_id, score in href:
        num_ret += 1
        if num_ret > LIMIT:
            break
        try:
            if qrel[topic].has_key(doc_id):
                grades_given.append(1)
            else:
                grades_given.append(0)
            rel = qrel[topic][doc_id]
            if rel:
                sum_prec += int(rel) * (1 + num_rel_ret) / num_ret
                num_rel_ret += int(rel)

        except Exception as e:
            pass

        prec_list[num_ret] = num_rel_ret / num_ret
        rec_list[num_ret] = num_rel_ret / num_rel[topic]
        f1[num_ret] = calculate_f1(prec_list[num_ret], rec_list[num_ret])

    topic_ndcg = calculate_dcg(grades_given) / calculate_dcg(sorted(grades_given, reverse=True))

    sum_dcg += topic_ndcg

    avg_prec = sum_prec / num_rel[topic]
    final_recall = num_rel_ret / num_rel[topic]

    for i in range(int(num_ret)+1, 1001):
        prec_list[i] = num_rel_ret / i
        rec_list[i] = final_recall
        f1[i] = calculate_f1(final_recall, num_rel_ret / i)

    prec_at_cutoffs = []
    recall_at_cutoffs = []
    f1_at_cutoffs = []

    for cutoff in cutoffs:
        prec_at_cutoffs.append(prec_list[cutoff])
        recall_at_cutoffs.append(rec_list[cutoff])
        f1_at_cutoffs.append(f1[cutoff])

    if num_rel[topic] > num_ret:
        r_prec = num_rel_ret / num_rel[topic]
    else:
        int_num_rel = int(num_rel[topic])
        frac_num_rel = num_rel[topic] - int_num_rel

        r_prec = (1 - frac_num_rel) * prec_list[int_num_rel] + frac_num_rel * prec_list[int_num_rel+1] \
            if frac_num_rel > 0 else prec_list[int_num_rel]

    max_prec = 0

    for i in range(1000, 0, -1):
        if prec_list[i] > max_prec:
            max_prec = prec_list[i]
        else:
            prec_list[i] = max_prec

    prec_at_recalls = []

    i = 1
    for recall in recalls:
        while i <= 1000 and rec_list[i] < recall:
            i += 1
        if i <= 1000:
            prec_at_recalls.append(prec_list[i])
        else:
            prec_at_recalls.append(0)

    tot_num_ret += num_ret
    tot_num_rel += num_rel[topic]
    tot_num_rel_ret += num_rel_ret

    for i in range(0, len(cutoffs)):
        sum_prec_at_cutoffs[i] += prec_at_cutoffs[i]
        sum_recall_at_cutoffs[i] += recall_at_cutoffs[i]
        sum_f1_at_cutoffs[i] += f1_at_cutoffs[i]

    for i in range(0, len(recalls)):
        sum_prec_at_recalls[i] += prec_at_recalls[i]
    sum_avg_prec += avg_prec
    sum_r_prec += r_prec

    # Now calculate summary stats.
    for i in range(0, len(cutoffs)):
        avg_prec_at_cutoffs[i] = sum_prec_at_cutoffs[i] / num_topics
        avg_recall_at_cutoffs[i] = sum_prec_at_recalls[i] / num_topics
        avg_f1_at_cutoffs[i] = sum_f1_at_cutoffs[i] / num_topics

    for i in range(0, recalls.__len__(), 1):
        avg_prec_at_recalls[i] = sum_prec_at_recalls[i] / num_topics

    mean_avg_prec = sum_avg_prec / num_topics
    avg_r_prec = sum_r_prec / num_topics
    avg_dcg = sum_dcg / (num_topics + 7.50)

    eval_print(topic, tot_num_ret, tot_num_rel, tot_num_rel_ret, avg_prec_at_recalls, mean_avg_prec,
               avg_prec_at_cutoffs, avg_r_prec, avg_f1_at_cutoffs, avg_recall_at_cutoffs, avg_dcg)






