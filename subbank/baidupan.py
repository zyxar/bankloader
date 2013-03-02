#!/usr/bin/env python

from urllib.request import urlopen, Request
from urllib.parse import unquote
from html.parser import HTMLParser
from re import compile as Pattern
from os.path import join
from .fetcher import Fetcher

class Klient(dict):
    """Client for Baidu Pan"""
    def __init__(self):
        self.pattern = Pattern(r'href=\"(http://.*)\" id=\"downFileButtom\"')

    def load(self, url):
        try:
            self.url = url
            self.sock = urlopen(url)
            html = self.sock.read().decode('utf-8')
            self.payload = HTMLParser().unescape(self.pattern.findall(html)[0])
            self.filename = Pattern(r'server_filename=\"([^\"]*)\"').findall(html)[0]
            self.sock.close()
        except Exception as e:
            print(repr(e))

    def download(self, path_prefix=''):
        try:
            req = Request(self.payload, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",  "Accept": "*/*", 'Connection': 'Keep-Alive'})
            req.add_header('Referer', self.url)
            self.sock = urlopen(req)
            Fetcher().retrieve(self.sock, join(path_prefix, self.filename))
            self.sock.close()
        except Exception as e:
            print(repr(e))


# if __name__ == '__main__':
#     client = Klient()
#     client.load('http://pan.baidu.com/share/link?shareid=352662&uk=4196951363')
#     client.download()
