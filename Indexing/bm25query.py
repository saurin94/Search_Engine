import ast
import json
import re

import math
from nltk.stem import PorterStemmer
from WriteRetrievalModels import WriteRetreivalModels

ps = PorterStemmer()


# Get DocIds Mapped to Numbers
f = open("docDict.txt", "r")
data = f.read()
docDictMap = json.loads(data)
f.close()
#-------------------------------------------------------------------------------------#
# Get avgLength of Docs
totalDocs = len(docDictMap)
totalwords = 0
for key,value in docDictMap.iteritems():
    totalwords += int(value[1])

avgLength = float(totalwords)/float(totalDocs)
#-------------------------------------------------------------------------------------#
# Load Catalog in  into termMap
termMap = {}
f1 = open("lastTry\\Catalog-ProperMergeSorted-1.txt", "r")
data = f1.readlines()
for i in data:
    d = i.split("=")
    k = d[0].split(" ")
    termMap[k[0]] = [k[1]] + [k[2].replace("\n", "")]
f1.close()
#-------------------------------------------------------------------------------------#
# Get StopWords
f = open("stoplist.txt", "r")
stopList = f.read().split("\n")
f.close()
#-------------------------------------------------------------------------------------#

class bm25Query(object):
    def __init__(self):

        global stopList
        global docDictMap
        global termMap
        global ps
        global avgLength
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
            # Query Preprocessing
            query = query.replace("Document", "")
            query = query.replace("will","")
            query = query.replace("report", "")
            data = query.lower().replace(",","").replace("."," ").replace("-"," ").replace("\"","").replace("(","")
            data = data.replace(")","").replace("\'"," ").replace("_"," ")

            terms = data.split()
            self.QueryProcess(terms, queryNo)

    def QueryProcess(self, terms, queryNo):
        docDict = {}
        f2 = open("lastTry\\InvertedIndex-ProperMergeSorted-1.txt", "r")
        # Iterate over each term
        for word in terms:
            if word not in stopList:
                newWord = ps.stem(word)
                StringData = []
                tfInQuery = 0
                for allterms in terms:
                    if newWord == ps.stem(allterms):
                        tfInQuery += 1
                if newWord in termMap:
                    # Get data from InvertedIndex-Final-1
                    f2.seek(int(termMap[newWord][0]))
                    finalData = f2.read(int(termMap[newWord][1])).split("=")[1:]

                    cfdf = finalData[0].split(",")
                    df = int(cfdf[0])
                    # Get all values : Docid : TFs
                    value = finalData[1].split(";")
                    for i in value:
                        docMapID = i.split(":")[0]
                        values = i.split(":")[1].replace("\n", "")
                        eachDocData = str(docMapID) + ":" + "[" + str(values) + "]"
                        StringData.append(eachDocData)
                    finalString = "{" + ",".join(StringData) + "}"
                    finalDict = ast.literal_eval(finalString)

                    # Retrieve DocID for each doc number
                    for key in finalDict:
                        newkey = str(key)
                        if newkey in docDictMap:
                            docId = docDictMap[newkey][0]
                            docLen = float(docDictMap[newkey][1])
                            tf = float(len(finalDict[key]))
                            if docDict.has_key(docId):
                                logVal = math.log10(84678.50/(df + 0.5))
                                middle = float((tf + (1.20*tf))/(tf + 1.20*(0.25 + 0.75*(docLen/avgLength))))
                                factor = float((tfInQuery + 10.0 * tf) / (tfInQuery + 10.0))
                                bm25 = factor * logVal * middle
                                prev = docDict[docId]
                                docDict[docId] = bm25 + prev
                            else:
                                logVal = math.log10(84678.50/ (df + 0.5))
                                middle = (tf + (1.20 * tf)) / (tf + 1.20 * (0.25 + 0.75 * (docLen / avgLength)))
                                factor = float((tfInQuery + 10.0 * tf) / (tfInQuery + 10.0))
                                bm25 = factor * logVal * middle
                                docDict[docId] = bm25
                        else:
                            print "DocId not found"
                else:
                    print "not found:", newWord

        r = WriteRetreivalModels()
        r.writeBm25file(queryNo, docDict)


h = bm25Query()
