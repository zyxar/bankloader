#!/usr/bin/env python

from urllib2 import urlopen
import json
from dbanklink import decrypt
import sys

class Loader():
    def __init__(self, url=None):
        self.data = None
        self.key = None
        self.files = []
        if url is not None:
            self.load(url)

    def reset(self):
        self.data = None
        self.key = None
        self.files = []

    def load(self, url):
        uu = urlopen(url)
        html = uu.read()
        data = html[html.find('var globallinkdata')+20:]
        data = data[:data.find('</script>')].strip()[:-1]
        self.data = json.loads(data)
        self.files = self.data['data']['resource']['files']
        self.key = self.data['data']['encryKey']
    
    def getdownloads(self):
        urls = []
        for ff in self.files:
            urls.append(decrypt(ff['downloadurl'], self.key))
        return urls

    def getxunleis(self):
        xuns = []
        for ff in self.files:
            xuns.append(decrypt(ff['xunleiurl'], self.key))
        return xuns
            
    def getnames(self):
        names = []
        for ff in self.files:
            names.append(ff['name'])
        return names

    def getdownload(self, n=0):
        return decrypt(self.files[n]['downloadurl'], self.key)

    def getxunlei(self, n=0):
        return decrypt(self.files[n]['xunleiurl'], self.key)

    def getname(self, n=0):
        return self.files[n]['name']

def main(argv=None):
    l = Loader(argv[0])
    for i in xrange(len(l.files)):
        print l.getname(i)
        print l.getdownload(i)
        print l.getxunlei(i)
        print

if __name__ == '__main__':
    main(sys.argv[1:])