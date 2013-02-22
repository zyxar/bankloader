#!/usr/bin/env python

from urllib2 import urlopen
from os.path import exists, getsize
from urllib import unquote
from fetcher import Fetcher, savefile


class Klient():
    """Klient: Download Helper for Kuaipan"""
    googlecharturl='http://chart.apis.google.com/chart?chs=%dx%d&choe=UTF-8&cht=qr&chld=L|5&chl='
    def __init__(self, url=None):
        self.url = url
        self.conn = None
        self.cont = None
        self.payload = None

    def seturl(self, url):
        self.url = url

    def connect(self):
        if self.url is not None:
            try:
                self.conn = urlopen(self.url, timeout = 5)
            except:
                self.conn = None
        return self.conn

    def meta(self):
        if self.conn is not None:
            self.info = self.conn.info()
        return self.info

    def parse(self):
        if self.cont is None:
            if self.conn is None:
                r = self.connect()
                if r is None:
                    return None
            self.cont = self.conn.read()
        idx = self.cont.find('var url = encodeURIComponent')+30
        self.payload = self.cont[idx:]
        idx = self.payload.find(');')-1
        self.payload = self.payload[:idx]
        return self.payload

    def download(self):
        if self.payload is None:
            self.parse()
        if self.payload is not None:
            uu = urlopen(self.payload, timeout=10)
            filename = uu.info().getheader('content-disposition').split('*=')[1].split('\'')
            encoding = filename[0]
            filename = unquote(filename[2]).decode(encoding)
            Fetcher().retrieve(uu, filename)
            uu.close()

    def qrcode(self, length=400, width=400):
        if self.payload is None:
            self.parse()
        if self.payload is not None:
            url = self.googlecharturl % (length, width)
            url += self.payload
            uu = urlopen(url)
            savefile('qrchart.png', uu.read())
            uu.close()


if __name__ == '__main__':
    client = Klient()
    client.seturl('http://www.kuaipan.cn/file/id_18920726803259181.htm')
    client.download()
