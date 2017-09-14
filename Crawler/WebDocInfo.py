class WebDocumentInfo(object):
    def __init__(self, docno, title, HTTPheader, html_Source, text, out_links, author, depth, url):
        self.docno = docno
        self.title = title
        self.HTTPheader = HTTPheader
        self.html_Source = html_Source
        self.text = text
        self.out_links = out_links
        self.author = author
        self.depth = depth
        self.url = url