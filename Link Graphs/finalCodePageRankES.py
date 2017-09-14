from collections import defaultdict
from sets import Set
import operator
from math import log

f = open('linkgraph_generated.txt', 'r')
data = f.readlines()

M = {}
L = {}
PR = {}
newPR = {}
P = Set()
S = Set()
perplexity_list = []


def p_value_calculate():
    calculate_value = 0.0
    for pg in PR.values():
        calculate_value += pg * log(pg, 2)

    return 2 ** (-1.0 * calculate_value)


def check_convergence(count):
    p_value = p_value_calculate()
    print str(count + 1) + " " + str(p_value)
    perplexity_list.append(p_value)
    if len(perplexity_list) > 4:
        if (int(perplexity_list[count])) == (int(perplexity_list[count - 1])) == (int(perplexity_list[count - 2])) == (
        int(perplexity_list[count - 3])):

            return True
        else:
            return False

    else:
        return False


line_number = 1
for line in data:
    try:
        single_line = line.split()
        line_number += 1
        if len(single_line) > 0:
            M[single_line[0]] = Set(single_line[1:])
            P.update(single_line)
    except Exception, e:
        print e, line_number
f.close()

N = float(len(P))

d = 0.85

for p in P:
    PR[p] = 1.0 / N  # initial value
    L[p] = 0.0

for in_link in M.values():
    for link in in_link:
        L[link] += 1.0

for link, outlink_count in L.items():
    if outlink_count == 0.0:
        S.add(link)

count = 0

while not (check_convergence(count)):
    sinkPR = 0.0
    for p in S:
        sinkPR += PR[p]

    for p in P:
        newPR[p] = (1.0 - d) / N
        newPR[p] += (d * sinkPR) / N
        if p in M:
            for q in M[p]:
                newPR[p] += (d * PR[q]) / L[q]

    for p in P:
        PR[p] = newPR[p]

    count += 1

i = 0
sorted_x = sorted(PR.items(), key=operator.itemgetter(1))
f = open("final_es_merged_inlink_count.txt", "a+")
for key, value in sorted_x:
    inlink_value = 0
    outlink_value = 0
    print value
    i += 1
    if i < 500:
        if key in M:
            inlink_value = len(M[key])
        if key in L:
            outlink_value = int(L[key])
        f.write(str(key) + " " + str(value) + " " + "inlink_count " + str(inlink_value) + " "  " outlink_count " +
                str(outlink_value) + "\n")
    else:
        break
f.close()
print "Houde Page Rank"
