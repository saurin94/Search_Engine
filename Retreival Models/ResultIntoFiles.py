import operator


class WriteIntoFile():
    def writeOkapiFile(self, queryNo, scoreList):
        with open("OkapiScores_all.txt", "a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                # if (count <= 1000):
                w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                    items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))

    def writeTfIDFFile(self, queryNo, scoreList):
        with open("tfIDFscores_all.txt", "a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                # if (count <= 1000):
                w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                    items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))

    def writebm25File(self, queryNo, scoreList):
        with open("bm25scores_all.txt", "a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                # if (count <= 1000):
                w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                    items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))

    def writeLaplace(self, queryNo, scoreList):
        with open("laplaceSmoothingScores_all.txt", "a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                # if (count <= 1000):
                w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                    items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))

    def writeUnigramJM(self, queryNo, scoreList):
        with open("JelinekMercerScores_all.txt", "a+") as w:
            count = 1
            sortedOkapi = sorted(scoreList.items(), key=operator.itemgetter(1), reverse=True)
            for items in sortedOkapi:
                # if (count <= 1000):
                w.write(str(queryNo) + " " + "Q0" + " " + str(items[0]) + " " + str(count) + " " + str(
                    items[1]) + " " + "Exp" + "\n")
                count = count + 1
        print("--------- query written into file - khatam -------------" + str(queryNo))
