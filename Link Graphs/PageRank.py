"""
Page Rank Algorithm:
- P is the set of all pages; |P| = N
- S is the set of sink nodes, i.e., pages that have no out links
- M(p) is the set of pages that link to page p
- L(q) is the number of out-links from page q
- d is the PageRank damping/teleportation factor; use d = 0.85 as is typical

foreach page p in P
  PR(p) = 1/N                          /* initial value */

while PageRank has not converged do
  sinkPR = 0
  foreach page p in S                  /* calculate total sink PR */
    sinkPR += PR(p)
  foreach page p in P
    newPR(p) = (1-d)/N                 /* teleportation */
    newPR(p) += d*sinkPR/N             /* spread remaining sink PR evenly */
    foreach page q in M(p)             /* pages pointing to p */
      newPR(p) += d*PR(q)/L(q)         /* add share of PageRank from in-links */
  foreach page p
    PR(p) = newPR(p)

return PR
"""
import math

# Global Variables declaration
import operator

inlinkDict = {}
outlinkDict = {}
prevhpr = 0
perplexityArray = []


def read_inlink_from_file():
    f = open('wt2g_inlinks/wt2g_inlinks.txt', 'r')
    global inlinkDict
    for inlinks_data in f.readlines():
        inlinks_list_maker = inlinks_data.split()
        inlink_key = inlinks_list_maker[0]
        if len(inlinks_data) > 0:
            inlink_value = set(inlinks_list_maker[1:])
        else:
            inlink_value = set([])
        if inlink_key in inlinkDict:
            prev = inlinkDict[inlink_key]
            prev.update(inlink_value)
            inlinkDict[inlink_key] = prev
        else:
            inlinkDict[inlink_key] = inlink_value
    print "Inlink Dict Length : ", len(inlinkDict)
    f.close()
    f = open("wt2g_inlink_count.txt", "a+")
    for key, value in inlinkDict.iteritems():
        f.write(str(key) + " " + str(len(value)) + "\n")
    f.close()


def read_outlink_from_inlink():
    global outlinkDict
    global inlinkDict
    for inlink_key, inlink_value in inlinkDict.iteritems():
        for link in inlink_value:
            if link in outlinkDict:
                prev = outlinkDict[link]
                prev.update([inlink_key])
                outlinkDict[link] = prev
            else:
                outlinkDict[link] = set([inlink_key])
    print "Outlink Dict Length : ", len(outlinkDict)


def get_sink_nodes():
    global sink_nodes_set
    outlinks_set = set()
    inlinks_set = set()
    for outlink in outlinkDict.keys():
        outlinks_set.add(outlink)
    for inlink in inlinkDict.keys():
        inlinks_set.add(inlink)
    sink_nodes_set = inlinks_set.difference(outlinks_set)
    print "Sink Nodes Length : ", len(sink_nodes_set)
    return sink_nodes_set


def converged(page_rank_dict):
    global perplexityArray
    global prevhpr
    if len(perplexityArray) == 4:
        if all(i < 1 for i in perplexityArray):
            return True
        else:
            perplexityArray = []
    hpr = 0.0

    for page, inlink_value in page_rank_dict.iteritems():
        if page_rank_dict[page] != 0.0:
            hpr += page_rank_dict[page] * math.log(page_rank_dict[page], 2)
    hprfinal = -1 * hpr
    perplexity = math.pow(2, hprfinal)
    perplexityArray.append(prevhpr-perplexity)
    prevhpr = perplexity
    return False


def page_rank():
    sink_nodes_set = get_sink_nodes()
    pageRankDict = {}
    n = len(inlinkDict)
    outlink_set = set(outlinkDict.keys())
    inlink_set = set(inlinkDict.keys())
    final_set = outlink_set.union(inlink_set)
    # print "Length of final set : ", len(final_set)
    for page in final_set:
        pageRankDict[page] = float(1.0/n)
    newPrDict = {}

    count = 0
    while not converged(pageRankDict):
        count += 1
        print "Iteration : ", count
        sinkPR = 0
        for each_page in sink_nodes_set:
            sinkPR += pageRankDict[each_page]

        d = 0.85
        for page, inlink_value in inlinkDict.iteritems():
            newPrDict[page] = (1.0 - d)/n
            newPrDict[page] += (d * sinkPR)/n

            for each_page in inlink_value:
                newPrDict[page] += d*pageRankDict[each_page]/len(outlinkDict[each_page])

        for page, inlink_value in inlinkDict.iteritems():
            pageRankDict[page] = newPrDict[page]

    i = 0
    sorted_x = sorted(pageRankDict.items(), key=operator.itemgetter(1) , reverse=True)
    f = open("final_wt2g_inlink_count.txt","a+")
    for key, value in sorted_x:
        i += 1
        if i < 500:
            if key in inlinkDict:
                f.write(str(key).ljust(20) + " " + str(len(inlinkDict[key])) + "\n")
            print str(key).ljust(14) + "  " + str(value)
        else:
            break
    f.close()
    print "Houde Page Rank"


read_inlink_from_file()
read_outlink_from_inlink()
page_rank()




