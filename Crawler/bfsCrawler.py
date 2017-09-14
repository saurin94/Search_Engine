import robotparser
from urlparse import urlparse
import BeautifulSoup
import html2text
import jsonpickle
import requests
import urlnorm
import WebDocInfo
import QueueSelf
import json

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_tables = True
# f = open("CrawledJsonRemaining.json", "a+")
f = open("Try20k.json", "a+")
depth = 0
count = 0


def check_robots_txt(url):
    host = urlparse(url)
    hostRobotUrl = host.scheme + "://" + host.netloc + "/robots.txt"
    rp = robotparser.RobotFileParser()
    rp.set_url(hostRobotUrl)
    try:
        rp.read()
        value = rp.can_fetch("*", url)
        return value
    except Exception, e:
        print "Robots parser Error :", e.message
        pass


def fetch_outlinks(ahrefs):
    newOutLinks = set()
    base_url = "https://en.wikipedia.org"
    for a in ahrefs:
        try:
            ahref = a['href'].lower()
            text = str(a.string).lower()
            # print "Ahref text:", text
            not_parseable_ressources = (".css", ".js", ".bmp", ".gif", ".jpeg", ".png", ".tiff", ".mid", ".mp2",
                                        ".mp3", ".mp4", ".wav", ".avi", ".mov", ".mpeg", ".ram", ".m4v", ".pdf",
                                        ".rm", ".smil", ".wmv", ".swf", ".wma", ".zip", ".rar", ".gz", ".csv",
                                        ".xls",
                                        ".ppt", ".doc", ".docx", ".exe", ".dmg", ".midi", ".mid", ".qt", ".txt",
                                        ".ram", ".jp"
                                        ".json", ".pdf\\", ".cfm", ".cms")
            if not urlparse(ahref).path.endswith(not_parseable_ressources):
                if "wiki" in ahref:
                    if "#" in ahref:  # Finding and removing URLs with # in them
                        ahref = ahref[:ahref.find("#")]
                        pass
                    elif "?" in ahref:  # Finding and removing URLs with ? in them
                        ahref = ahref[:ahref.find("?")]
                        pass
                    elif ":" in ahref:  # Finding and removing URLs with : in them
                        ahref = ahref[:ahref.find(":")]
                        pass
                    elif "//" in ahref:  # Finding and removing URLs with // in them
                        ahref = ahref[:ahref.find("//")]
                        pass
                    elif ahref == "/wiki/Main_Page":  # Finding and removing URLs of Main page of Wiki
                        pass
                    elif "united" in ahref or "states" in ahref or "u.s" in ahref or "illegal" \
                            in ahref or "immig" in ahref \
                            or "donald" in ahref or "trump" in ahref:
                        newUrl = a['href']
                        finalUrl = base_url + newUrl
                        finalUrl = urlnorm.norm(finalUrl).encode("utf-8", "ignore")
                        newOutLinks.add(finalUrl)
                else:
                    parseNonWikiURl = urlparse(a['href'])
                    pathHref = parseNonWikiURl.path
                    if ahref[:2] == "//":  # Finding and removing URLs with // in them
                        pass
                    elif ahref[0] == "/" or ahref[0] == ".":
                        pass
                    elif ahref[:-1] == "/":
                        ahref = ahref[:-1]
                    elif "index" in ahref or "youtube" in ahref or "rgu" in ahref or "book" in ahref \
                            or "american" in ahref or "chapter" in ahref or "language" in ahref \
                            or "journal" in ahref or "uscg" in ahref or "subscribe" in ahref or "/us" in ahref\
                            or "edition" in ahref:
                        pass
                    elif "#" in ahref:  # Finding and removing URLs with # in them
                        ahref = ahref[:ahref.find("#")]
                        pass
                    elif "unit" in ahref or "state" in ahref or "u.s" in ahref or "illeg" \
                            in ahref or "immig" in ahref or "donald" in ahref or "trump" in \
                            ahref or "us-news" in ahref or "usa" in ahref:
                        newUrl = a['href']
                        finalUrl = newUrl
                        try:
                            finalUrl = urlnorm.norm(newUrl)
                        except Exception, e:
                            # print e.message
                            pass
                        else:
                            finalUrl = newUrl
                        finalUrl = (finalUrl).encode("utf-8", "ignore")
                        # print "______________________________"
                        # print "non-wiki links : ", finalUrl
                        # print "______________________________"
                        newOutLinks.add(finalUrl)
        except KeyError, e:
            # print "ahref keyerror : ", e.message
            pass
    return newOutLinks


def fetch_contents(url, depth):
    try:
        t = requests.Session()
        t.max_redirects = 3
        # try:
        r = t.get(url, headers={'accept': 'text/html'}, allow_redirects=True, timeout=10)
        # try:
        httpheaders = r.headers
        contentType = r.headers.get("content-type").decode("utf-8", "ignore")
        # print "content type : ", contentType
        # print "status code : ", r.status_code
        if "text" in contentType and r.status_code == 200:
            # print "into fetching :"
            response = r.text
            soup = BeautifulSoup.BeautifulSoup(response)
            try:
                docNo = urlnorm.norm(url)
                docID = docNo.encode("utf-8", "ignore")
            except Exception, e:
                print "URL cannot be normalized, error :", e.message
                pass
            else:
                docID = url
            docIDFinal = docID.replace("https", "http", 1)
            # print type(soup.title.text.encode("utf-8","ignore"))
            title = soup.title.text.encode("utf-8", "ignore").strip()
            # httpheaders = str(httpheaders).encode("utf-8", "ignore").strip()
            httpheaders = str(', '.join("%s=%r" % (key, val) for (key, val) in httpheaders.iteritems()))
            text = r.text.encode("utf-8", "ignore").strip()
            htmlSource = soup.find('html').text
            newText = soup.parse
            ahrefs = soup.findAll('a')
            outlinks = fetch_outlinks(ahrefs)
            print("Fetched URL : " + str(url))
            # Make object of these contents
            if len(outlinks) > 0:
                print("Outlinks are present for this url")
                w = WebDocInfo.WebDocumentInfo(docno=docIDFinal, title=title, HTTPheader=httpheaders,
                                               html_Source=text,
                                               text=htmlSource, out_links=outlinks, author="Saurin", depth=depth,
                                               url=url)
                return w
            else:
                print("No Outlinks")
                w = WebDocInfo.WebDocumentInfo(docno=docIDFinal, title=title, HTTPheader=httpheaders,
                                               html_Source=text,
                                               text=htmlSource, out_links=[], author="Saurin", depth=depth,
                                               url=url)
                return w
    except Exception, e:
        print "Couldnt get page error :", e
        pass


def write_into_file(w):
    global count
    count += 1
    s = jsonpickle.encode(w, unpicklable=False)
    t = jsonpickle.decode(s)
    json.dump(t, f)
    f.write("\n")
    print "Count :" + str(count)
    print "______________________________________________"


def bfs_algorithm(queue, visitedUrls, listOfOutlinksDepthWise, depth):
    while (queue.size() != 0):
        # Stop when visitedUrl set reaches 22000
        if len(visitedUrls) > 27000:
            break
        else:
            print("depth :" + str(depth))
            url = queue.dequeue()
            print("url to be checked : " + str(url))
            if url not in visitedUrls:
                value = check_robots_txt(url)
                if value:
                    visitedUrls.add(url)
                    # Fetch contents of URL
                    w = fetch_contents(url, depth)
                    if w is not None:
                        if len(w.out_links) > 0:
                            woutlinks = w.out_links
                            write_into_file(w)
                            listOfOutlinksDepthWise += list(woutlinks)
                        else:
                            pass
                    else:
                        pass

                else:
                    print "Skipped this Link"
            else:
                print "URL already visited"


def load_seed_urls():
    global depth
    visitedUrls = set()
    outlinksMap = {}
    # Load seed URLS into queue
    seed1 = "https://en.wikipedia.org/wiki/Immigration_to_the_United_States"
    seed2 = "https://en.wikipedia.org/wiki/Illegal_immigration"
    seed3 = "https://www.theguardian.com/us-news/2017/jan/27/donald-trump-executive-order-immigration-full-text"
    seed4 = "https://www.whitehouse.gov/the-press-office/2017/01/27/executive-order-protecting-nation-foreign-terrorist-entry-united-states"
    seed5 = "https://www.usatoday.com/story/news/world/2017/01/28/what-you-need-know-trumps-refugee-ban/97183112/"
    seed6 = "https://www.usatoday.com/story/news/politics/2017/02/20/donald-trump-set-to-issue-new-revised-travel-ban-against-majority-muslim-countries/98167072/"
    seed7 = "http://www.cnn.com/2017/01/28/politics/donald-trump-executive-order-immigration-reaction/index.html"
    queue = QueueSelf.Queue()
    queue.enqueue(seed1)
    queue.enqueue(seed2)
    queue.enqueue(seed3)
    queue.enqueue(seed4)
    queue.enqueue(seed5)
    queue.enqueue(seed6)
    queue.enqueue(seed7)
    listOfOutlinksDepthWise = []
    while len(visitedUrls) <= 27000:
        print("crawled websites : ", len(visitedUrls))
        if queue.size() == 0:

            print("-----------------------------------------------------------")
            print("Queue empty")
            print("Visited links : ", len(visitedUrls))
            print("--------------------------------------------------------------")
            if len(listOfOutlinksDepthWise) != 0:
                for i in listOfOutlinksDepthWise:
                    queue.enqueue(i)
                listOfOutlinksDepthWise = []  # Once the queue is loaded, empty this list.
                bfs_algorithm(queue, visitedUrls,
                                  listOfOutlinksDepthWise, depth)
                depth += 1
        else:
            bfs_algorithm(queue, visitedUrls, listOfOutlinksDepthWise,
                              depth)
            depth += 1


def load_remaining_seed_urls():
    global depth
    visitedUrls = set()
    outlinksMap = {}
    # Load seed URLS into queue
    f = open("remainingOutlinks.txt", "r")
    t = f.read()
    outlinkset = eval(t)
    f.close()
    queue = QueueSelf.Queue()
    for i in outlinkset:
        queue.enqueue(i)
    listOfOutlinksDepthWise = []
    while len(visitedUrls) <= 5500:
        print("crawled websites : ", len(visitedUrls))
        if queue.size() == 0:
            print("-----------------------------------------------------------")
            print("Queue empty")
            print("Visited links : ", len(visitedUrls))
            print("--------------------------------------------------------------")
            if len(listOfOutlinksDepthWise) != 0:
                for i in listOfOutlinksDepthWise:
                    queue.enqueue(i)
                listOfOutlinksDepthWise = []  # Once the queue is loaded, empty this list.
                bfs_algorithm(queue, visitedUrls, outlinksMap,
                              listOfOutlinksDepthWise, depth)
                depth += 1
        else:
            bfs_algorithm(queue, visitedUrls, outlinksMap, listOfOutlinksDepthWise,
                          depth)
            depth += 1

# load_remaining_seed_urls()
load_seed_urls()