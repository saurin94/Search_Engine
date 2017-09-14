import ast
import robotparser
from urlparse import urlparse
import BeautifulSoup
import html2text
import jsonpickle
import requests
import time
import urlnorm
import WebDocInfo
import PriorityQueue
import json
#from reppy.robots import Robots


# PseudoCode for Crawler
''' 1. Load seed URLS into Queue with same Priority.
       (a) Wikipedia Link (b) Wikipedia Link (c) Google links
    2. For each URL in queue, apply BFS algorithm as follows :
       i.   Dequeue queue, get URL
       ii.  Check robots.txt of host URL 
       iii. If it can be fetched , fetch contents and out_links (on basis of keywords) 
       iv.  Maintain set of out_links for each depth 
       v.   Create object of URL :
              a. URL - normalized
              b. URL - not normalized
              c. Title 
              d. Out_links
              e. HTTPheader
              f. html_Source
              g. text (clean_html)
              h. author
              i. depth 
       vi.  Write the object into file as json 
       vi.  Once queue is empty for a depth , add all the out_links of next depth saved in queue with same priority
    3. Repeat this for each URL 
'''


h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_tables = True
f = open("Try20kPriority.json", "a+")
depth = 0
count = 0


def load_seed_urls():
    global depth
    visitedUrls = set()
    # Load seed URLS into queue
    # seed1 = "https://en.wikipedia.org/wiki/Immigration_to_the_United_States"
    seed1 = "https://www.drupal.org"
    seed2 = "https://en.wikipedia.org/wiki/Illegal_immigration"
    seed3 = "https://www.theguardian.com/us-news/2017/jan/27/donald-trump-executive-order-immigration-full-text"
    seed4 = "https://www.whitehouse.gov/the-press-office/2017/01/27/executive-order-protecting-nation-foreign-terrorist-entry-united-states"
    seed5 = "https://www.usatoday.com/story/news/world/2017/01/28/what-you-need-know-trumps-refugee-ban/97183112/"
    seed6 = "https://www.usatoday.com/story/news/politics/2017/02/20/donald-trump-set-to-issue-new-revised-travel-ban-against-majority-muslim-countries/98167072/"
    seed7 = "http://www.cnn.com/2017/01/28/politics/donald-trump-executive-order-immigration-reaction/index.html"
    queue = PriorityQueue.priority_queue()
    # All seed URLs are prioritized to One
    queue.enqueue(seed1, 1)
    queue.enqueue(seed2, 1)
    queue.enqueue(seed3, 1)
    queue.enqueue(seed4, 1)
    queue.enqueue(seed5, 1)
    queue.enqueue(seed6, 1)
    queue.enqueue(seed7, 1)
    # For each depth : A list of Out_links will be maintained which will be loaded into the queue
    #                  after the out_links of previous depth are over.
    listOfOutlinksDepthWise = []
    while len(visitedUrls) <= 36000:
        print("crawled websites : ", len(visitedUrls))
        # If for a depth , if the queue is empty, load all the URLs for next depth into the queue
        if queue.size() == 0:
            print("-----------------------------------------------------------")
            print("Queue empty")
            print("Visited links : ", len(visitedUrls))
            print("--------------------------------------------------------------")
            if len(listOfOutlinksDepthWise) != 0:
                # All links in outlinks are given the same priority as 1
                for i in listOfOutlinksDepthWise:
                    queue.enqueue(i, 1)
                listOfOutlinksDepthWise = []  # Once the queue is loaded, empty this list.
                bfs_algorithm(queue, visitedUrls, listOfOutlinksDepthWise, depth)
                depth += 1
        else:
            # If the queue is not empty , fetch details for the current URL in the queue
            bfs_algorithm(queue, visitedUrls, listOfOutlinksDepthWise, depth)
            depth += 1


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
                value, crawlDelay = check_robots_txt(url)
                print "Value : " + str(value) + " | " + "Delay : " + str(crawlDelay)
                if value and crawlDelay <= 1 or crawlDelay is None:
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


def check_robots_txt(url):
    # Get host of URL
    host = urlparse(url)
    # Make Robots.txt for this host
    hostRobotUrl = host.scheme + "://" + host.netloc + "/robots.txt"
    rp = robotparser.RobotFileParser()
    rp.set_url(hostRobotUrl)
    try:
        # Read Robots.txt and Check if the page can be fetched or not
        rp.read()
        # Crawl delay - to be added. ----------------------
        value = rp.can_fetch("*", url)
        crawlDelay = 0
        # parser = Robots.fetch(domain + '/robots.txt')
        # crawlDelay = parser.agent('*').delay
        # print crawlDelay
        # print "IN here", h.text

        return (value, crawlDelay)
    except Exception, e:
        print "Robots parser Error :", e.message
        pass


def fetch_contents(url, depth):
    try:
        # Added check for time. -------------------------
        time.sleep(1)
        t = requests.Session()
        t.max_redirects =3
        r = t.get(url, headers={'accept': 'text/html'}, allow_redirects=True, timeout=10)
        httpheaders = r.headers
        contentType = r.headers.get("content-type").decode("utf-8", "ignore")
        if "text" in contentType and r.status_code == 200:
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
            title = soup.title.text.encode("utf-8", "ignore").strip()
            httpheaders = str(', '.join("%s=%r" % (key, val) for (key, val) in httpheaders.iteritems()))
            text = r.text.encode("utf-8", "ignore").strip()
            htmlSource = soup.find('html').text
            ahrefs = soup.findAll('a')
            outlinks = fetch_outlinks(ahrefs)
            print " Fetched URL : " + str(url)
            # Make object of these contents
            if len(outlinks) > 0:
                print " Out links are present for this url"
                w = WebDocInfo.WebDocumentInfo(docno=docIDFinal, title=title, HTTPheader=httpheaders,
                                               html_Source=text,
                                               text=htmlSource, out_links=outlinks, author="Saurin", depth=depth,
                                               url=url)
                return w
            else:
                print"No Out links"
                w = WebDocInfo.WebDocumentInfo(docno=docIDFinal, title=title, HTTPheader=httpheaders,
                                               html_Source=text,
                                               text=htmlSource, out_links=[], author="Saurin", depth=depth,
                                               url=url)
                return w
    except Exception, e:
        print "Couldnt get page error :", e
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


def write_into_file(w):
    global count
    count += 1
    # Create a json of the Object of WebDocInfo
    s = jsonpickle.encode(w, unpicklable=False)
    t = jsonpickle.decode(s)
    # Dump the json into the file
    json.dump(t, f)
    f.write("\n")
    print "Count :" + str(count)
    print "______________________________________________"


# def load_remaining_seed_urls():
#     global depth
#     visitedUrls = set()
#     outlinksMap = {}
#     # Load seed URLS into queue
#     f = open("remainingOutlinks.txt", "r")
#     t = f.read()
#     outlinkset = eval(t)
#     f.close()
#     queue = PriorityQueue.priority_queue()
#     for i in outlinkset:
#         queue.enqueue(i, 1)
#     listOfOutlinksDepthWise = []
#     while len(visitedUrls) <= 5500:
#         print("crawled websites : ", len(visitedUrls))
#         if queue.size() == 0:
#             print("-----------------------------------------------------------")
#             print("Queue empty")
#             print("Visited links : ", len(visitedUrls))
#             print("--------------------------------------------------------------")
#             if len(listOfOutlinksDepthWise) != 0:
#                 for i in listOfOutlinksDepthWise:
#                     queue.enqueue(i)
#                 listOfOutlinksDepthWise = []  # Once the queue is loaded, empty this list.
#                 bfs_algorithm(queue, visitedUrls, outlinksMap,
#                               listOfOutlinksDepthWise, depth)
#                 depth += 1
#         else:
#             bfs_algorithm(queue, visitedUrls, outlinksMap, listOfOutlinksDepthWise,
#                           depth)
#             depth += 1


# load_remaining_seed_urls()

load_seed_urls()

