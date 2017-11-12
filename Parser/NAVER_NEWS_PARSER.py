import requests, threading
from bs4 import BeautifulSoup as parse

class Parser:
    def __init__(self, url="http://news.naver.com/"):
        self.url = url
        self.interval = 0
        self.maxDepth = 20

        self.dataDict = {}

    def getUrls(self, parser):
        total = 0
        try:
            for url, text in [[x['href'], x.text] for x in parser.select("a")]:
                if not url:
                    pass

                elif url[0] == "#":
                    pass

                elif url[0] == "/":
                    if self.url[:-1]+url not in self.dataDict.keys():
                        self.dataDict[self.url[:-1]+url] = {"text": text, "data": None}
                        total += 1

                elif url[:5] == "http":
                    if url not in self.dataDict.keys():
                        self.dataDict[url] = {"text": text, "data": None}
                        total += 1

                else:
                    pass
        finally:
            return total

    def getPage(self, url):
        _temp = requests.get(url).text
        _parser = parse(_temp, 'html.parser')

        threading.Thread(target=self.getUrls, args=(_parser,)).start()
        return self.parseNumbers(url)

    def parseNumbers(self, data):
        return 1

    def worker(self, index, depth=0):
        if depth >= self.maxDepth:
            return -1

        mine = self.dataDict[index]

        if mine['data'] is None:
            mine['data'] = self.getPage(index)

            print(depth, index, len(self.dataDict.keys()))
            return True
        else:
            return False

    def run(self):
        self.dataDict[self.url] = {"text": "네이버뉴스", "data": None}

        keep = True
        depth = 0

        while keep:
            keys = [x for x in self.dataDict.keys()]
            for url in keys:
                _t = self.worker(url, depth)

                if _t is -1:
                    print("Max Depth")
                    keep = False
                    break
            depth += 1