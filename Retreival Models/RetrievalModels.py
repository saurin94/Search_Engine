import operator
from ResultIntoFiles import WriteIntoFile

class RetrievalModel():

    def okapiTfcalculate(self,queryNo, docDict):
        h = WriteIntoFile()
        h.writeOkapiFile(queryNo,docDict)

    def bm25calculate(self,queryNo, docDict):
        h = WriteIntoFile()
        h.writebm25File(queryNo,docDict)

    def tfIdfcalculate(self,queryNo,docDict):
        h = WriteIntoFile()
        h.writeTfIDFFile(queryNo,docDict)

    def laplaceSmoothing(self,queryNo,docDict):
        h = WriteIntoFile()
        h.writeLaplace(queryNo,docDict)

    def unigramJM(self,queryNo,docDict):
        h = WriteIntoFile()
        h.writeUnigramJM(queryNo,docDict)




