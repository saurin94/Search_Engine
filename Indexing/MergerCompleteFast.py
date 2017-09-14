import os
import operator

# -------------------------------------------------------------------------------------#
f = open('set.txt', "r")
d = f.read()
f.close()
# -------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------#
catalogMap = {}
catalogDir = "lastTry\\catalog4\\"
invertedDir = "lastTry\\index4\\"
# -------------------------------------------------------------------------------------#
vocab = set()

for each_file in os.listdir(catalogDir):
    f = open(catalogDir + each_file,"r")
    data = f.readlines()
    for i in data:
        d = i.split("=")
        k = d[0].split(" ")
        vocab.add(k[0])

print "new vocab",len(vocab)

for each_file in os.listdir(catalogDir):
    termMap = {}
    f = open(catalogDir + each_file, "r")
    data = f.readlines()
    for i in data:
        d = i.split("=")
        k = d[0].split(" ")
        termMap[k[0]] = [k[1]] + [k[2].replace("\n", "")]
        catalogMap[each_file] = termMap


class MergingIndexes(object):
    global catalogMap
    global termMap
    global vocab

    # -------------------------------------------------------------------------------------#
    def __init__(self):

        finalInverted = open("lastTry\\InvertedIndex-MergedTF.txt", "a+")
        finalCatalog = open("lastTry\\Catalog-MergedTF.txt", "a+")
        # -------------------------------------------------------------------------------------#
        seekValue = 0
        count = 0

        print("Entering into vocab loop ")
        for term in vocab:
            # Text Preprocess
            a = str(term).replace(",", "").replace("(", "").replace(")", "").replace("\'", "")
            StringData = []
            df = 0
            cf = 0
            # -------------------------------------------------------------------------------------#
            for file, value in catalogMap.iteritems():
                if a in value:

                    eachValue = value[a]
                    seeker = int(eachValue[0])
                    reader = int(eachValue[1])

                    # print file,seeker,reader
                    f = open(invertedDir + file, "r")
                    f.seek(seeker)
                    data = f.read(reader).split("=")[1:]

                    cfdf = data[0].split(";")
                    df += int(cfdf[0].split(",")[0])
                    cf += int(cfdf[0].split(",")[1])
                    docValues = data[1].replace("\n", "")
                    docValues = docValues.rstrip(";")

                    final = docValues.split(";")
                    for i in final:
                        StringData.append(i)
                    f.close()
            termInfoLen = {}
            termInfo = {}
            allSelectedDoc = []
            for termDetails in StringData:
                idMap = termDetails.split(":")[0]
                allSelectedDoc.append(idMap)
                valueMap = len(termDetails.split(":")[1].split(","))
                termInfoLen[idMap] = valueMap
                termInfo[idMap] = termDetails.split(":")[1]
            # -------------------------------------------------------------------------------------#
            # Sorting Indexes in descending Order
            sortedtermInfo = sorted(termInfoLen.items(), key=operator.itemgetter(1), reverse=True)
            stringToAppend = []
            for everyValue in sortedtermInfo:
                termId = everyValue[0]
                stringToAppend.append(str(termId) + ":" + str(termInfo[termId]))
            # -------------------------------------------------------------------------------------#
            writeData = ';'.join(stringToAppend)
            finalInverted.write(str(a) + "=" + str(df) + "," + str(cf) + "=" + str(writeData))
            finalInverted.write("\n")
            lengthData = len(str(a) + "=" + str(df) + "," + str(cf) + "=" + str(writeData)) + 1
            finalCatalog.write(str(a) + " " + str(seekValue) + " " + str(lengthData))
            finalCatalog.write("\n")
            seekValue += lengthData + 1
            count += 1
            print count
            # -------------------------------------------------------------------------------------#

        finalInverted.close()
        finalCatalog.close()

merging = MergingIndexes()