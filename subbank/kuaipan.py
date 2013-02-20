#!/usr/bin/env python

from urllib.request import urlopen
from urllib.parse import unquote
from os.path import exists, getsize, join
from .fetcher import Fetcher#, savefile

class Klient():
    """Klient: Download Helper for Kuaipan"""
    # googlecharturl='http://chart.apis.google.com/chart?chs=%dx%d&choe=UTF-8&cht=qr&chld=L|5&chl='
    def __init__(self, url=None):
        self.conn = None
        self.cont = None
        self.payload = None
        self.load(url)

    def load(self, url):
        self.url = url
        if self.url is not None:
            try:
                self.conn = urlopen(self.url, timeout = 5)
            except:
                self.conn = None
        return self.parse()

    def meta(self):
        if self.conn is not None:
            self.info = self.conn.info()
        return self.info

    def parse(self):
        try:
            self.cont = self.conn.read()
        except:
            return None
        idx = self.cont.find(b'var url = encodeURIComponent')+30
        if idx == 29:
            raise KeyError
        self.payload = self.cont[idx:]
        idx = self.payload.find(b');')-1
        self.payload = self.payload[:idx]
        if isinstance(self.payload, bytes):
            self.payload = self.payload.decode('UTF-8')
        return self.payload

    def download(self, path_prefix=''):
        if self.payload is None:
            self.parse()
        if self.payload is not None:
            uu = urlopen(self.payload, timeout=10)
            filename = unquote(uu.info().get('content-disposition').split('*=')[1].split('\'')[2])
            filename = join(path_prefix, filename)
            Fetcher().retrieve(uu, filename)
            uu.close()

    # def qrcode(self, length=400, width=400):
    #     if self.payload is None:
    #         self.parse()
    #     if self.payload is not None:
    #         url = self.googlecharturl % (length, width)
    #         url += self.payload
    #         uu = urlopen(url)
    #         savefile('qrchart.png', uu.read())
    #         uu.close()

# if __name__ == '__main__':
#     client = Klient()
#     client.seturl('http://www.kuaipan.cn/file/id_18920726803259181.htm')
#     client.download()
