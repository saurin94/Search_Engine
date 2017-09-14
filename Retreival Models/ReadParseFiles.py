import os
from elasticsearch import Elasticsearch
from lxml import etree as E
import json

class ReadFromFile(object):
    def __init__(self):
        directory = "D:\\IR\\IR_data\\AP_DATA" + "\\" + "ap89_collection\\"
        JsonDict = {}
        # Open files in the corpus folder
        fileSize = 1
        count = 0
        for each_file in os.listdir(directory):
            if each_file != 'readme':
                with open(directory + each_file, 'r') as f:
                    data = f.readlines()

                # Convert data to string
                data_new = ' '.join(data)
                # Add root elements for XMLParser
                data_final = "<root>" + data_new + "</root>"
                print each_file

                # Create Parser for XMLParser
                parser = E.XMLParser(recover=True, encoding='latin1')
                # Tree for each file
                root = E.fromstring(data_final, parser=parser)
                # Get children
                children = root.getchildren()

                # Create Json array for each doc
                for child in children:
                    finalText = ""
                    for grandchild in child:
                        if grandchild.tag == 'DOCNO':
                            finalDocNo = grandchild.text.replace(" ", "")
                            JsonDict[grandchild.tag] = finalDocNo
                            count = count + 1
                        if grandchild.tag == 'TEXT':
                            grandchild.text.lstrip()
                            grandchild.text.rstrip()
                            finalText += grandchild.text
                            JsonDict['text'] = finalText
                    value = json.dumps(JsonDict)
                    self.sendDataToElasticSearch(finalDocNo,value)
                    print ("successful")
                # print count
                    print "*********************************************************************************"
    print ("----------------------------------------Done ---------------------------------------------------------")
    print ("----------------------------------------Done ---------------------------------------------------------")

    def sendDataToElasticSearch(self,docno,jsondict):
        # r = requests.get('http://localhost:9200')
        es = Elasticsearch()
        res = es.index(index='ap_dataset', doc_type='HW1', id=docno, body=jsondict)
        print(res['created'])

result = ReadFromFile()








