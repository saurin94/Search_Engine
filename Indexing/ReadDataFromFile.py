import json
import os
from lxml import etree as E
from Tokenize import Tokenize

file_name = 0
doc_no = 0
count = 1



def writeToFile(finalDocNo,wordDictWithOffset):
    global count
    # global catalogCount
    catalogCount = 1
    print finalDocNo.split("-")
    index = "invertedIndex"
    catalog = "catalog"
    index_file = index + str(count) + ".txt"
    catalog_file = catalog + str(count) + ".txt"
    f1 = open(index_file,"a+")
    f2 = open(catalog_file, "a+")
    seekValue = 0
    for key, value in wordDictWithOffset.iteritems():
        f1.write(str(key) + "==" + str(value) + "\n")
        value1 = len(str(key)) + 2 + len(str(value)) + 1
        catalogOffset = value1
        f2.write(str(key) + " " + str(seekValue) + " " + str(catalogOffset) + "\n")
        seekValue += catalogOffset + 1
        catalogCount += 1
    count = count + 1
    f1.close()
    f2.close()
    ReadFromFile()


class ReadFromFile(object):
    def __init__(self):
        global file_name, doc_no
        h = Tokenize()
        total = 0
        directory = "D:\\IR\\IR_data\\AP_DATA" + "\\" + "ap89_collection\\"
        # Open files in the corpus folder
        wordDictWithOffset = {}
        termMap = {}
        for each_file in os.listdir(directory):
            if each_file != 'readme':
                file1 = int(each_file[2:])
            # print directory + "ap"+str(file1-1)
            if (os.path.exists(directory + "ap"+str(file1-1))):
                os.remove(directory + "ap"+str(file1-1))
            if each_file != 'readme' and file_name <= file1:
                with open(directory + each_file, 'r') as f:
                    data = f.read()
                # Add root elements for XMLParser
                data_final = "<root>" + data + "</root>"
                print each_file

                # Create Parser for XMLParser
                parser = E.XMLParser(recover=True, encoding='latin1')
                # Tree for each file
                root = E.fromstring(data_final, parser=parser)
                # Get children
                children = root.getchildren()
                # print len(children),type(children),children
                for child in children:
                    finalText = ""
                    if total < 1000:
                        for grandchild in child:
                            if grandchild.tag == 'DOCNO':
                                total += 1
                                # print total
                                finalDocNo = grandchild.text.replace(" ", "")
                            if grandchild.tag == 'TEXT':
                                grandchild.text.lstrip()
                                grandchild.text.rstrip()
                                finalText += grandchild.text
                        if ((file_name * 10000) + doc_no) < ((file1 * 10000) + int(finalDocNo.split("-")[1])):
                            h.tokenizeText(finalText, finalDocNo, termMap, wordDictWithOffset)
                    else:
                        file_name = int(finalDocNo.split("-")[0][2:])
                        doc_no = int(finalDocNo.split("-")[1])
                        writeToFile(finalDocNo,wordDictWithOffset)

