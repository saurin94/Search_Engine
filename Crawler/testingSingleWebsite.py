import time
import urllib2
import html2text
import BeautifulSoup
import urlnorm

import WebDocInfo

url1 = "http://www.washingtonpost.com/politics/new-super-pac-hopes-to-give-cover-to-pro-immigration-republicans/2012/11/16/c3070b74-300b-11e2-a30e-5ca76eeec857_story.html"
url2 = "https://www.theguardian.com/us-news/2017/jan/27/donald-trump-executive-order-immigration-full-text"
url3 = "https://www.usatoday.com/story/news/world/2017/01/28/what-you-need-know-trumps-refugee-ban/97183112/"
not_parseable_ressources = (
".avi", ".mkv", ".mp4", ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".iso", ".rar", ".tar", ".tgz", ".zip", ".dmg", ".exe")
import QueueSelf
import requests

queue = QueueSelf.Queue()
import urlparse
import robotparser

queue.enqueue(url3)
queue.enqueue(url2)
rp = robotparser.RobotFileParser()
h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_tables = True


def fetchOutlinks(ahrefs):
    newOutLinks = set()
    base_url = "https://en.wikipedia.org"
    for a in ahrefs:
        try:
            ahref = a['href'].lower()
            not_parseable_ressources = (".avi", ".mkv", ".mp4", ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".iso", ".rar", ".tar", ".tgz", ".zip", ".dmg", ".exe")
            if not urlparse.urlparse(ahref).path.endswith(not_parseable_ressources):
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
                    elif "united" in ahref or "states" in ahref or "u.s" in ahref or "illegal" in ahref or "immig" in ahref or "donald" in ahref or "trump" in ahref:
                            newUrl = a['href']
                            finalUrl = base_url + newUrl
                            finalUrl = urlnorm.norm(finalUrl).encode("utf-8", "ignore")
                            newOutLinks.add(finalUrl)
                    else:
                        if ahref[:2] == "//":  # Finding and removing URLs with // in them
                            pass
                        elif "index" in ahref or "youtube" in ahref or "rgu" in ahref or "book" in ahref or "american" in ahref:
                            pass
                        elif "#" in ahref:  # Finding and removing URLs with # in them
                            ahref = ahref[:ahref.find("#")]
                            pass
                        elif "united" in ahref or "states" in ahref or "u.s" in ahref or "illegal" in ahref or "immig" in ahref or "donald" in ahref or "trump" in ahref:
                            newUrl = a['href']
                            finalUrl = newUrl
                            print "outlinks:",finalUrl
                            finalUrl = urlnorm.norm(finalUrl).encode("utf-8", "ignore")
                            newOutLinks.add(finalUrl)
        except KeyError, e:
            pass
    return newOutLinks

while queue.size() > 0:
    url = queue.dequeue()
    host = urlparse.urlparse(url)
    print "end url:", not urlparse.urlparse(url).path.endswith(not_parseable_ressources)
    robots = str(host.scheme) + "://" + str(host.netloc) + "/robots.txt"
    print robots
    rp.set_url(robots)
    k = rp.read()
    val = rp.can_fetch("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", url)
    print val
    if val == True:
        if "wiki" in url:
            time.sleep(1)

        # Request for the page
        try:
            r = requests.Session()
            r.max_redirects = 3
            try:
                request = r.get(url, allow_redirects=True, timeout=10)
                contentType = request.headers
                contentTypeOriginal = request.headers.get("content-type")
                print contentTypeOriginal
                if ("text" in contentTypeOriginal or "html" in contentTypeOriginal) and request.status_code == 200:
                    print("----------------> Fetching URL : " + str(url))
                    response = request.content
                    # print response
                    soup = BeautifulSoup.BeautifulSoup(response)
                    docNo = "\"" + url + "\""
                    title = "\"" + str(soup.title).decode("utf-8", "ignore").strip() + "\""
                    httpheaders = str('\'\'\'') + str(contentType).strip() + str('\'\'\'')
                    text = str('\'\'\'') + h.handle(str(soup).decode("utf-8", "ignore")).strip() + str('\'\'\'')
                    htmlSource = str('\'\'\'') + str(soup).strip() + str('\'\'\'')
                    ahrefs = soup.findAll('a')
                    outlinks = fetchOutlinks(ahrefs)
                    # Make object of these contents
                    depth = "0"
                    if len(outlinks) != 0:
                        print outlinks
                        w = WebDocInfo.WebDocumentInfo(docId=docNo, title=title, HTTPheader=httpheaders,
                                                       rawHtml=htmlSource,
                                                       cleanHtml=text, outlinks=outlinks, author="saurin", depth=depth,
                                                       url=docNo)
                    else:
                        print("No outlinks, Not a proper page")
                        pass
                else:
                    print "Nothing to fetch"
                    pass
            except Exception, e:
                print "TimeOut Error :", e.message
                pass

        except urllib2.HTTPError, e:
            print "Error Code:", e.code
            print "Error Message:", e.message
            pass
