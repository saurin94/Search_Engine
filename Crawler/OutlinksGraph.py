import json


class OutlinksGraph(object):

    def __init__(self):
        out_links_map = {}
        visited = set()
        try:
            f = open("Try20k.json", "r")
            for line in f:
                try:
                    jsonNode = json.loads(line)
                    # normlURL = Get url as it is
                    normURL = str(jsonNode['docno'].encode("utf-8", "ignore"))
                    # finalNormUrl = lowercase normUrl
                    if normURL[-1] == "/":
                        normURL = normURL[:-1]
                    finalNormUrl = normURL.lower()
                    # Check finalNormURL is in visited
                    finalOutlinks = jsonNode['out_links']
                    if finalNormUrl not in visited:
                        visited.add(finalNormUrl)
                        out_links_map[finalNormUrl] = finalOutlinks
                        print "Added link : ", finalNormUrl
                        print "----------------Success--------------"
                except Exception, e:
                    print "Cant load json for current line ,Error :", e
        except Exception, e:
            print "File Open Error :", e
        finally:
            print "Out link map has total of key of Urls as : ", len(out_links_map)
            w = open("LinkGraph.json", "a+")
            json.dump(out_links_map, w, indent=4)
            w.close()

OutlinksGraph()