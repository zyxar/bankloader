#!/usr/bin/env python

from urllib.request import urlopen
from .dbanklink import DBDecoder
import sys
import json

class Klient():
    decoder = DBDecoder()
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
        data = html[html.find(b'var globallinkdata')+20:]
        data = data[:data.find(b'</script>')].strip()[:-1]
        try:
            self.data = json.loads(data.decode('UTF-8'))
        except:
            sys.stderr.write('failure in loading data.\n')
            sys.stderr.flush()
            return False
        else:
            self.files = self.data['data']['resource']['files']
            self.key = self.data['data']['encryKey']
        uu.close()
        return True
    
    def getdownloads(self):
        urls = []
        for ff in self.files:
            urls.append(self.decoder.decrypt(ff['downloadurl'], self.key))
        return urls

    def getxunleis(self):
        xuns = []
        for ff in self.files:
            xuns.append(self.decoder.decrypt(ff['xunleiurl'], self.key))
        return xuns
            
    def getnames(self):
        names = []
        for ff in self.files:
            names.append(ff['name'])
        return names

    def getdownload(self, n=0):
        return self.decoder.decrypt(self.files[n]['downloadurl'], self.key)

    def getxunlei(self, n=0):
        return self.decoder.decrypt(self.files[n]['xunleiurl'], self.key)

    def getname(self, n=0):
        return self.files[n]['name']
