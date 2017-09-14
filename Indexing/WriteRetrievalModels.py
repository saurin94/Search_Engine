import operator


class WriteRetreivalModels(object):
    def writeOkapiFile(self,queryNo,scoreList):
        with open("okapiScores-HW2.txt","a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                if (count <= 1000):
                    w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                        items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))

    def writetfIDFfile(self,queryNo,scoreList):
        with open("tfIDF-HW2.txt","a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                if (count <= 1000):
                    w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                        items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))

    def writeBm25file(self,queryNo,scoreList):
        with open("bm25-HW2.txt","a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                if (count <= 1000):
                    w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                        items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))

    def writeLaplace(self,queryNo,scoreList):
        with open("unigramLaplace-HW2.txt","a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                if (count <= 1000):
                    w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                        items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))

    def writeProximity(self, queryNo, scoreList):
        with open("proximity-HW2.txt", "a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                if (count <= 1000):
                    w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                        items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))


