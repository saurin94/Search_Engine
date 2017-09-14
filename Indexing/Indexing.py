import json
import os

import operator

from Tokenize import Tokenize
count = 1
termMap ={}
vocab = set()

def writeToFile(wordDictWithOffset):

    global count
    index_file = str(count) + ".txt"
    catalog_file = str(count) + ".txt"
    f1 = open("lastTry\\index4\\" + index_file,"a+")
    f2 = open("lastTry\\catalog4\\" + catalog_file, "a+")

    seekValue = 0

    for key,value in wordDictWithOffset.iteritems():
        s = sorted(value.items(), key=lambda x: (len(x[1])), reverse=True)
        string2 = ""
        df = 0
        cf = 0
        for i in s:
            tf = len(i[1])
            df += 1
            cf += len(i[1])
            string2 += str(i[0]) + ":" + str(i[1]).replace("]", "").replace("[", "").replace(" ", "")+"-"+str(tf)+";"
        string1 = str(df) + "," + str(cf) + "="
        string3 = string1 + string2
        f1.write(str(key)+ "=" + string3 + "\n")
        value = len(str(key)+ "=" + string3 + "\n")
        catalogOffset = value
        f2.write(str(key) + " " + str(seekValue) + " " + str(catalogOffset) + "\n")
        value += 1
        seekValue += catalogOffset + 1
    count = count + 1
    f1.close()
    f2.close()


class Indexing(object):
    global vocab
    def indexingAsIs(self):
        h = Tokenize()
        directory = "newDocId\\"
        global termMap
        # Open files in the corpus folder
        for each_file in os.listdir(directory):
            wordDictWithOffset = {}
            with open(directory + each_file,"r") as r:
                data = r.read()
                dataDict = json.loads(data)
                print each_file
                for docNo, text in dataDict.iteritems():
                    positionNew = 1
                    h.tokenizeText(text,docNo,wordDictWithOffset,positionNew,vocab)
            writeToFile(wordDictWithOffset)
        f = open("set.txt","w")
        f.write(str(vocab))
        f.close()
        #MergerCompleteFast.MergingIndexes()

h = Indexing()
h.indexingAsIs()