import math
import matplotlib.pyplot as plt
import sys

__author__ = 'saurin_shah'


def input_validation(arg):
    print_queries = 0

    if len(arg) < 2 or len(arg) > 3:
        print "Usage: trec_eval [-q] <qrel_file> <trec_file>"
        sys.exit(2)

    if len(arg) == 3:
        if arg[0] == '-q':
            print_queries = 1
        else:
            print "Usage: trec_eval [-q] <qrel_file> <trec_file>"
            sys.exit(2)
        qrel_file = arg[1]
        trec_file = arg[2]

    if len(arg) == 2:
        if arg[0] == '-q':
            print "Usage: trec_eval [-q] <qrel_file> <trec_file>"
            sys.exit(2)
        else:
            qrel_file = arg[0]
            trec_file = arg[1]
    return (print_queries, qrel_file, trec_file)


def plot_graph(prec_array, query_num):
    recall_array = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    plt.plot(recall_array,prec_array)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.grid(True)
    plt.title('Interpolated Recall - Precision Averages')
    name = "prec_recall_plot_qid_"+str(query_num)
    plt.savefig("./graphs/%s.png" % name)
    plt.close()


def eval_print(topic, ret, rel, ret_rel, avg_prec_at_recalls, map, avg_prec_at_cutoffs, rp, avg_f1_at_cutoffs,
               avg_recall_at_cutoffs, avg_ndcg):

    plot_graph(avg_prec_at_recalls, topic)

    print "Queryid (Num):    " + str(topic)
    print "Total number of documents over all queries"
    print "    Retrieved:    " + str(ret)
    print "    Relevant:     " + str(rel)
    print "    Rel_ret:      " + str(int(ret_rel))

    print "Interpolated Recall - Precision Averages:"
    print "    at 0.00       %0.4f" % avg_prec_at_recalls[0]
    print "    at 0.10       %0.4f" % avg_prec_at_recalls[1]
    print "    at 0.20       %0.4f" % avg_prec_at_recalls[2]
    print "    at 0.30       %0.4f" % avg_prec_at_recalls[3]
    print "    at 0.40       %0.4f" % avg_prec_at_recalls[4]
    print "    at 0.50       %0.4f" % avg_prec_at_recalls[5]
    print "    at 0.60       %0.4f" % avg_prec_at_recalls[6]
    print "    at 0.70       %0.4f" % avg_prec_at_recalls[7]
    print "    at 0.80       %0.4f" % avg_prec_at_recalls[8]
    print "    at 0.90       %0.4f" % avg_prec_at_recalls[9]
    print "    at 1.00       %0.4f" % avg_prec_at_recalls[10]

    print "Average precision (non-interpolated) for all rel docs(averaged over queries)"
    print "                  %0.4f" % map
    print "                  Precision  Recall  F1-Measure"
    print "  At    5 docs:   %0.4f      %0.4f   %0.4f" % (avg_prec_at_cutoffs[0], avg_recall_at_cutoffs[0], avg_f1_at_cutoffs[0])
    print "  At   10 docs:   %0.4f      %0.4f   %0.4f" % (avg_prec_at_cutoffs[1], avg_recall_at_cutoffs[1], avg_f1_at_cutoffs[1])
    print "  At   20 docs:   %0.4f      %0.4f   %0.4f" % (avg_prec_at_cutoffs[2], avg_recall_at_cutoffs[2], avg_f1_at_cutoffs[2])
    print "  At   50 docs:   %0.4f      %0.4f   %0.4f" % (avg_prec_at_cutoffs[3], avg_recall_at_cutoffs[3], avg_f1_at_cutoffs[3])
    print "  At  100 docs:   %0.4f      %0.4f   %0.4f" % (avg_prec_at_cutoffs[4], avg_recall_at_cutoffs[4], avg_f1_at_cutoffs[4])
    print "R-Precision (precision after R (= num_rel for a query) docs retrieved):"
    print "    Exact:        %0.4f" % rp
    print "nDCG value for all the relevant documents at k = 5, 10, 20, 50, 100:"
    print "                  %0.4f" % avg_ndcg
    print "----------------------------------------------------------------------------------------------"


def calculate_ndcg(n_dcg_list):
    n_dcg = (2 ** dcg_list[0] - 1) / math.log(2, 2)
    for i in range(1, len(n_dcg_list)):
        n_dcg += (2 ** n_dcg_list[i] - 1) / math.log(i + 2, 2)
    return n_dcg

if __name__ == '__main__':
    q_opted_option, QREL, TREC = input_validation(sys.argv[1:])

    with open(QREL, 'r') as qrel_file:
        qrel_data = qrel_file.readlines()

    # take the values from each line and put them in a data structure
    # qrel is a dict, whose keys are topicIDs and whose values are
    # another hash. This hash has keys as docIDs and values that are relevance values

    dummy = 0
    q_rel = {}
    doc_rel = {}
    num_rel = {}

    for line in qrel_data:
        line.rstrip()
        topic = line.split('()')[0]
        doc_id = line.split('()')[2]
        rel = float(line.split('()')[3])

        if topic in q_rel:
            if doc_id in q_rel[topic]:
                q_rel[topic][doc_id] = max(q_rel[topic][doc_id], rel)
            else:
                q_rel[topic].update({doc_id: rel})
        else:
            q_rel.update({topic: {doc_id: rel}})

        if topic in num_rel:
            if rel > 0:
                num_rel[topic] += 1
        else:
            if rel > 0:
                num_rel[topic] = 1
            else:
                num_rel[topic] = 0

    with open(TREC, 'r') as t:
        trec_data = t.readlines()

    trec = {}

    for line in trec_data:
        (topic, dummy, doc_id, dummy, score, dummy) = line.split('<:>')
        doc_score_map = {}
        if topic in trec:
            doc_score_map = trec[topic]
        doc_score_map[doc_id] = float(score)
        trec[topic] = doc_score_map

    # Initializing arrays
    recalls = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    cutoffs = [5, 10, 20, 50, 100]

    num_topics = 0
    temp_doc_rel_map = {}
    sum_avg_prec = 0
    sum_r_prec = 0
    sum_avg_f1 = 0
    sum_dcg = 0

    total_num_ret = 0
    total_num_rel = 0
    total_num_ret_rel = 0
    sum_prec_at_cutoff = {}
    sum_recall_at_cutoff = {}
    sum_prec_at_recalls = {}
    sum_f1_at_cutoffs = {}

    trec_keys = trec.keys()
    trec_keys.sort()

    for topic in trec_keys:
        if not (topic in num_rel):
            continue
        num_topics += 1
        temp_doc_rel_map = trec[topic]

        prec_list = {}
        recall_list = {}
        dcg_list = []

        num_ret = 0
        num_ret_rel = 0
        sum_prec = 0
        sum_f1 = 0

        sorted_temp_doc_rel = sorted(temp_doc_rel_map.items(), key=lambda x: x[1], reverse=True)

        for item in sorted_temp_doc_rel:
            doc_id = item[0]
            num_ret += 1
            if doc_id in q_rel[topic]:
                bin_rel = 1 if q_rel[topic][doc_id] > 0 else 0
                dcg_list.append(bin_rel)
                sum_prec += bin_rel * (1 + num_ret_rel) / float(num_ret)
                num_ret_rel += bin_rel
            else:
                dcg_list.append(0)

            prec_list[num_ret] = num_ret_rel/float(num_ret)
            recall_list[num_ret] = num_ret_rel/float(num_rel[topic])

            if num_ret >= 1000:
                break

        avg_prec = sum_prec / float(num_rel[topic])
        print "dcg", dcg_list.__len__()

        if max(dcg_list) == 0:
            dcg_value = 0.0
        else:
            dcg_value = calculate_ndcg(dcg_list) / calculate_ndcg(sorted(dcg_list, reverse=True))
            sum_dcg += dcg_value

        avg_f1 = float(sum_f1/num_rel[topic])

        final_recall = num_ret_rel / float(num_rel[topic])
        count = num_ret
        while count <= 1000:
            prec_list[count] = (num_ret_rel / float(count))
            recall_list[count] = (final_recall)
            count += 1

        prec_at_cutoffs = []
        recall_at_cutoffs = []
        f1_at_cutoffs = []

        for cutoff in cutoffs:
            prec_at_cutoffs.append(prec_list[cutoff])
            recall_at_cutoffs.append(recall_list[cutoff])

        for i in range(len(cutoffs)):
            a = prec_at_cutoffs[i]
            b = recall_at_cutoffs[i]
            if a > 0 and b > 0:
                f1_at_cutoffs.append((2 * a * b) / float(a + b))
            else:
                f1_at_cutoffs.append(0.0)

        r_prec = 0
        if num_rel[topic] > num_ret:
            r_prec = num_ret_rel / float(num_rel[topic])
        else:
            int_num_rel = int(num_rel[topic])
            frac_num_rel = num_rel[topic] - int_num_rel

            if frac_num_rel > 0:
                r_prec = (1 - frac_num_rel) * prec_list[int_num_rel] + frac_num_rel * prec_list[int_num_rel + 1]
            else:
                r_prec = prec_list[int_num_rel]

        max_prec = 0
        size_prec_list = prec_list.__len__()

        for i in range(size_prec_list, 0, -1):
            if prec_list[i] > max_prec:
                max_prec = prec_list[i]
            else:
                prec_list[i] = max_prec

        prec_at_recalls = []
        i = 1
        for recall in recalls:
            while i <= recall_list.__len__() and recall_list[i] < recall:
                i += 1
            if i <= prec_list.__len__():
                prec_at_recalls.append(prec_list[i])
            else:
                prec_at_recalls.append(0)

        # Print stats on a per query basis if requested.
        if q_opted_option == 1:
            print "q = 1"
            eval_print(topic, num_ret, num_rel[topic], num_ret_rel, prec_at_recalls, avg_prec, prec_at_cutoffs,
                       r_prec, f1_at_cutoffs, recall_at_cutoffs, dcg_value)

        total_num_ret += num_ret
        total_num_rel += int(num_rel[topic])
        total_num_ret_rel += num_ret_rel

        for i in range(0, len(cutoffs), 1):
            if i in sum_prec_at_cutoff:
                sum_prec_at_cutoff[i] += prec_at_cutoffs[i]
            else:
                sum_prec_at_cutoff[i] = prec_at_cutoffs[i]

            if i in sum_recall_at_cutoff:
                sum_recall_at_cutoff[i] += recall_at_cutoffs[i]
            else:
                sum_recall_at_cutoff[i] = recall_at_cutoffs[i]

            if i in sum_f1_at_cutoffs:
                sum_f1_at_cutoffs[i] += f1_at_cutoffs[i]
            else:
                sum_f1_at_cutoffs[i] = f1_at_cutoffs[i]

        for i in range(0, len(recalls), 1):
            if i in sum_prec_at_recalls:
                sum_prec_at_recalls[i] += prec_at_recalls[i]
            else:
                sum_prec_at_recalls[i] = prec_at_recalls[i]

        sum_avg_prec += avg_prec
        sum_r_prec += r_prec
        sum_avg_f1 += avg_f1

    avg_prec_at_cutoffs = []
    avg_prec_at_recalls = []
    avg_f1_at_cutoffs = []
    avg_recall_at_cutoffs = []

    for i in range(0, len(cutoffs), 1):
        avg_prec_at_cutoffs.append(sum_prec_at_cutoff[i] / num_topics)
        avg_recall_at_cutoffs.append(sum_recall_at_cutoff[i] / num_topics)
        avg_f1_at_cutoffs.append(sum_f1_at_cutoffs[i] / num_topics)

    for i in range(0, len(recalls), 1):
        avg_prec_at_recalls.append(sum_prec_at_recalls[i] / num_topics)

    mean_avg_prec = float(sum_avg_prec) / float(num_topics)
    avg_r_prec = sum_r_prec / num_topics
    avg_f1_all = float(sum_avg_f1 / num_topics)
    avg_dcg = float(sum_dcg / num_topics)

    eval_print(topic, total_num_ret, total_num_rel, total_num_ret_rel,
               avg_prec_at_recalls, mean_avg_prec, avg_prec_at_cutoffs,
               avg_r_prec, avg_f1_at_cutoffs, avg_recall_at_cutoffs, avg_dcg)
