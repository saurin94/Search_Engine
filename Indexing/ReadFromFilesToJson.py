import json
import os
from lxml import etree as E
import collections

class WriteDataToJson(object):
    def __init__(self):

        directory = "D:\\IR\\IR_data\\AP_DATA" + "\\" + "ap89_collection_read\\"
        total = 0
        docDict = {}
        count = 1
        for each_file in os.listdir(directory):
            fileDict = {}
            if each_file != 'readme':
                with open(directory + each_file, 'r') as f:
                    data = f.read()
                # Convert data to string
                # Add root elements for XMLParser
                data_final = "<root>" + data + "</root>"
                # print each_file

                # Create Parser for XMLParser
                parser = E.XMLParser(recover=True, encoding='latin1')
                # Tree for each file
                root = E.fromstring(data_final, parser=parser)
                # Get children
                children = root.getchildren()
                # Into each children
                for child in children:
                    finalText = ""
                    for grandchild in child:
                        if grandchild.tag == 'DOCNO':
                            finalDocNo = grandchild.text.replace(" ", "")
                        if grandchild.tag == 'TEXT':
                            grandchild.text.lstrip()
                            grandchild.text.rstrip()
                            finalText += grandchild.text
                        docDict[count] = [finalDocNo,len(finalText.split(" "))]
                    fileDict[count] = finalText
                    count+=1
                    print count

        with open("docDict.txt","w+") as w:
            json.dump(docDict,w,indent=0)


