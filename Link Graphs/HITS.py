from sets import Set
import random
from ordered_set import OrderedSet
import operator
from math import log
from math import pow
from math import sqrt

# Root Set
rootSet = OrderedSet()

# Base Set
base_set = Set()

# Dict
inlink_dict = {}
outlink_dict = {}

# Hub and Authority
authority = {}
hub = {}


perplexity_authority = []
perplexity_hub = []


def get_authority_value():
    entropy = 0.0
    for pg in authority.values():
        if pg != 0.0:
            entropy += pg*log(pg, 2)

    return 2**(-1.0*entropy)


def get_hub_value():
    entropy = 0.0
    for pg in hub.values():
        if pg != 0.0:
            entropy += pg*log(pg, 2)

    return 2**(-1.0*entropy)


def did_converged(count):

    authority_value  = get_authority_value()
    hubs_value = get_hub_value()
    perplexity_authority.append(authority_value)
    perplexity_hub.append(hubs_value)
    if len(perplexity_authority) > 4 and len(perplexity_hub) > 4:
        if(((int(perplexity_authority[count])) == (int(perplexity_authority[count-1])) == (int(perplexity_authority[count-2])) ==
            (int(perplexity_authority[count-3]))) and ((int(perplexity_hub[count])) == (int(perplexity_hub[count - 1])) ==
                (int(perplexity_hub[count - 2])) == (int(perplexity_hub[count - 3])))):
            print str(count+1) + " " + str(authority_value) + " " + str(hubs_value)
            return True
        else:
            return False

    else:
        return False


def load_inlink_graph():
    f = open('Files\\inlinks.txt', 'r')
    l = f.readlines()

    lineNumb = 1
    for line in l:
        try:
            line_final = line.strip('\n').split('<:>')
            line_final = [each_line for each_line in line_final if each_line != '']
            inlink_dict[line_final[0]] = Set(line_final[1:])
            lineNumb += 1
        except Exception, e:
            print e, lineNumb

    f.close()


def load_outlink_graph():
    f = open('Files\\outlinks.txt', 'r')
    l = f.readlines()

    for line in l:
        try:
            line_final = line.strip('\n').split('<:>')
            line_final = [each_line for each_line in line_final if each_line != '']
            outlink_dict[line_final[0]] = Set(line_final[1:])

        except Exception, e:
            print e

    f.close()


def load_root_set():
    f = open('Files\\rootSet.txt', 'r')
    l = f.readlines()

    for line in l:
        try:
            rootSet.add(line.strip())

        except Exception, e:
            print e + "ou"

    f.close()


def base_set_methods():
    d = 200

    base_set.update(rootSet)

    # Expanding Base Set
    f = open('Files\\rootSet.txt', 'r')
    l = f.readlines()

    ln = 1

    for line in l:
        try:
            p = line.strip()
            if len(base_set) > 10000:
                break
            if p in outlink_dict:
                base_set.update(outlink_dict[p])

            if p in inlink_dict:
                inlink_set = inlink_dict[p]
                if len(inlink_set) <= d:
                    base_set.update(inlink_set)
                else:
                    base_set.update(random.sample(inlink_set, d))

        except Exception, e:
            print e, "ou"

    f.close()

    print len(base_set)


def hits():
    for p in base_set:
        authority[p] = 1.0
        hub[p] = 1.0

    count = 0

    while not (did_converged(count)):
        if count > 100:
            break
        norm = 0.0
        for p in base_set:
            authority[p] = 0.0
            if p in inlink_dict:
                for q in inlink_dict[p]:
                    if q in hub:
                        authority[p] += float(hub[q])
            norm += float(pow(authority[p], 2.0))

        norm = float(sqrt(norm))

        for p in base_set:
            authority[p] = float(authority[p]) / norm

        norm = 0.0
        for p in base_set:
            hub[p] = 0.0
            if p in outlink_dict:
                for r in outlink_dict[p]:
                    if r in authority:
                        hub[p] += float(authority[r])
            norm += float(pow(hub[p], 2.0))

        norm = float(sqrt(norm))

        for p in base_set:
            hub[p] = float(hub[p]) / norm

        count += 1


def to_print():
    sorted_authority = sorted(authority.iteritems(), key=operator.itemgetter(1), reverse=True)
    sorted_hub = sorted(hub.iteritems(), key=operator.itemgetter(1), reverse=True)

    print "Authority Links"
    f = open("final_es_links_top_500.txt", "a+")
    for j in range(500):
        inlink_count = 0
        outlink_count = 0
        url = sorted_authority[j]
        final_url = url[0]
        if final_url in inlink_dict.keys():
            inlink_count = int(len(inlink_dict[final_url]))
        if final_url in outlink_dict.keys():
            outlink_count = int(len(outlink_dict[final_url]))
        f.write(str(sorted_authority[j]) + "\t" + "inlink_count : " + str(inlink_count) + " outlink_count: " +
                str(outlink_count) + "\n")
    f.close()

    print "Hub Links"

    f = open("hub_links_top_500.txt", "a+")
    for j in range(500):
        inlink_count = 0
        outlink_count = 0
        url = sorted_hub[j]
        final_url = url[0]
        if final_url in inlink_dict:
            inlink_count = int(len(inlink_dict[final_url]))
        if final_url in outlink_dict:
            outlink_count = int(len(outlink_dict[final_url]))
        f.write(str(sorted_hub[j]) + "\t" + "inlink_count : " + str(inlink_count) + " outlink_count: " +
                str(outlink_count) + "\n")
    f.close()


load_inlink_graph()
load_outlink_graph()
load_root_set()
base_set_methods()
hits()
to_print()
