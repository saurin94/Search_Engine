import ast
import json
import math
from nltk.stem import PorterStemmer
import heapq

import TermStatistics
from WriteRetrievalModels import WriteRetreivalModels

# -------------------------------------------------------------------------------------#
ps = PorterStemmer()
# -------------------------------------------------------------------------------------#
# Get DocIds Mapped to Numbers
f = open("docDict.txt", "r")
data = f.read()
docDictMap = json.loads(data)
f.close()
# -------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------#
# Load Catalog in  into termMap
termMap = {}
f1 = open("lastTry\\Catalog-ProperMergeSorted-1.txt", "r")
data = f1.readlines()
for i in data:
    d = i.split("=")
    k = d[0].split(" ")
    termMap[k[0]] = [k[1]] + [k[2].replace("\n", "")]
f1.close()
# -------------------------------------------------------------------------------------#
# Get StopWords
f = open("stoplist.txt", "r")
stopList = f.read().split("\n")
f.close()
# -------------------------------------------------------------------------------------#
C = 1500


def calculateProximityValue(HashMap):
    a = 0
    array = []
    flags = []
    for key, value in HashMap.iteritems():
        array.append(value)
        a += len(value)
        flags.append(1)
    # print a
    h = []
    rangeheap = []
    for termArray in array:
        heapq.heappush(h, termArray[0])
    while a > 0:
        for flag in flags:
            if flag == 0:
                index = flags.index(flag)
                # print index
                heapq.heappush(h, array[index][0])
        largest = heapq.nlargest(1, h)[0]
        smallest = heapq.nsmallest(1, h)[0]
        range = largest - smallest
        heapq.heappush(rangeheap, range)
        heapq.heappop(h)
        indexFlag = 0
        indexGet = 0
        for termArray in array:
            if smallest in termArray:
                termArray.remove(smallest)
                termArray.append(smallest)
                indexGet = indexFlag
            indexFlag += 1
        i = 0
        while i != len(flags):
            if i == indexGet:
                flags[i] = 0
            else:
                flags[i] = 1
            i += 1
        a -= 1
    # print heapq.nsmallest(1, rangeheap)[0]
    return heapq.nsmallest(1,rangeheap)[0]


class ProximityQuery(object):
    def __init__(self):

        global stopList
        global docDictMap
        global termMap
        global ps
        global C
        # Get all queries

        directory = "D:\\IR\\IR_data\\AP_DATA" + "\\" + "query_desc.51-100.short.txt"
        with open(directory, "r") as r:
            allQueries = r.readlines()
        # Get all queries in ascending order in dictionary
        queryDict = {}

        for each_query in allQueries:
            queryDict[int(each_query.split()[0].replace(".", ""))] = ' '.join(each_query.split()[1:])
        # Iterate through each query.
        for queryNo, query in queryDict.iteritems():
            docDict = {}
            query = query.replace("Document", "")
            query = query.replace("will", "")
            query = query.replace("report", "")
            query = query.replace("identify","")
            data = query.lower().replace(",", "").replace(".", " ").replace("-", " ").replace("\"", "").replace("(", "")
            data = data.replace(")", "").replace("\'", " ").replace("_", " ")
            terms = data.split()
            # print queryNo
            self.QueryProcess(terms, queryNo, docDict)
            # print docDict
            # print (queryNo,"------------------------------------------------------------------------------")

    # -------------------------------------------------------------------------------------#
    def QueryProcess(self, terms, queryNo, docDict):
        importantWordDict = {}
        f2 = open("lastTry\\InvertedIndex-ProperMergeSorted-1.txt", "r")
        # Iterate over each term
        totalterms = 0
        for word in terms:
            if word not in stopList:
                totalterms +=1
                newWord = ps.stem(word)
                StringData = []
                if newWord in termMap:
                    # Get data from InvertedIndex-Final-1
                    f2.seek(int(termMap[newWord][0]))
                    finalData = f2.read(int(termMap[newWord][1])).split("=")[1:]
                    cfdf = finalData[0].split(",")
                    df = int(cfdf[0])
                    cf = int(cfdf[1])
                    logvalue = math.log10(84678.0 / df)
                    if df >= 2 and cf >= 2 and logvalue >= 0.36401:
                        importanceValue = math.log10(84678.0 / df)
                        importantWordDict[newWord] = importanceValue
                        # sortedValue = sorted(importantWordDict.items(), key=operator.itemgetter(1),reverse=True)

                    # Get all values : Docid : TFs
                    value = finalData[1].split(";")
                    for i in value:
                        docMapID = i.split(":")[0]
                        values = i.split(":")[1].replace("\n", "")
                        eachDocData = str(docMapID) + ":" + "[" + str(values) + "]"
                        StringData.append(eachDocData)
                    finalString = "{" + ",".join(StringData) + "}"
                    finalDict = ast.literal_eval(finalString)

                    #                     # Retrieve DocID for each doc number
                    for key in finalDict:
                        newkey = str(key)
                        if newkey in docDictMap:
                            docId = docDictMap[newkey][0]
                            docLen = float(docDictMap[newkey][1])
                            positions = (finalDict[key])
                            if docDict.has_key(docId):
                                termstats = TermStatistics.TermStats(word, positions)
                                docDict[docId] += [termstats]
                                # print docDict[docId]
                            else:
                                termstats = TermStatistics.TermStats(word, positions)
                                docDict[docId] = [termstats]
                        else:
                            print "DocId not found"
                else:
                    print "not found: ", newWord

        # print len(docDict)
        finalDocIdMap = {}
        # Proximity Algo
        for docId, termstat in docDict.iteritems():
            HashMap = {}
            termInDoc = len(termstat)
            totaltermsIndoc = len(termstat)
            while termInDoc > 0:
                    for classval in termstat:
                        HashMap[termInDoc] = classval.positions
                        termInDoc -= 1
            # print "HashMap ",docId,HashMap

            RangeOfWindow = calculateProximityValue(HashMap)
            finalDocIdMap[docId] = (C - RangeOfWindow)*totaltermsIndoc/(439.0 + 157812.0)

        # print("Done with heapify bc")
        r = WriteRetreivalModels()
        r.writeProximity(queryNo, finalDocIdMap)


# -------------------------------------------------------------------------------------#

h = ProximityQuery()
