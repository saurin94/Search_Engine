import ast
import json

import re

import math
from nltk.stem import PorterStemmer

ps = PorterStemmer()
termMap = {}
f = open("docDict.txt", "r")
data = f.read()
docDict = json.loads(data)
f.close()

# print len(docDict)
f1 = open("lastTry\\Catalog-MergedTF.txt", "r")
data = f1.readlines()
for i in data:
    d = i.split("=")
    k = d[0].split(" ")
    termMap[k[0]] = [k[1]] + [k[2].replace("\n", "")]
f1.close()

f3 = open("in.0.50.txt", "r")
data = f3.read()
allTerm = data.split("\n")
f3.close()
# print allTerm
f2 = open("lastTry\\InvertedIndex-MergedTF.txt", "r")
total = 0

StringData = []
# h = "Chudnovsky circumference Dalhousie Borwien"
# h = h.lower().split(" ")
dfterms = []
cfterms = []
logdfvalue = []
for s in allTerm:
    new = ps.stem(s)
    if new in termMap:
        f2.seek(int(termMap[new][0]))
        finalData = f2.read(int(termMap[new][1])).split("=")[1:]
        cfdf = finalData[0].split(",")
        df = int(cfdf[0])
        dfterms.append(df)
        cf = int(cfdf[1])
        print s + " " + str(df) + " " + str(cf)

f2.close()
