#!/usr/bin/env python

from urllib2 import urlopen, Request
from os.path import exists, getsize
from StringIO import StringIO
import sys

def status(percent):
    bar_size = 40
    percent = int(percent*100)
    if percent > 100:
        percent = 100
    dots = bar_size * percent / 100
    plus = ''
    if dots < 40:
        plus = '>'
    bar = '=' * dots+plus
    bar = '{0:>3}%[{1:<40}]'.format(percent, bar)
    sys.stdout.write('\r'+bar)
    sys.stdout.flush()

class Fetcher():
    block_sz = 32 * 1024
    def __init__(self, url=None):
        self.url = url

    def fetch(self, url=None):
        payload = url or self.url
        if payload is not None:
            ss = StringIO()
            uu = urlopen(payload)
            meta = uu.info()
            filename = payload.split('/')[-1]
            dld = 0
            size = int(meta.getheader('content-length'))
            if exists(filename) and getsize(filename) == size:
                print "File %s already exists." % filename
            else:
                print "Downloading: %s. Bytes: %d" % (filename, size)
                while True:
                    buf = uu.read(self.block_sz)
                    if not buf:
                        break
                    dld += len(buf)
                    ss.write(buf)
                    status(dld*1./size)
                print
                ff = open(filename, 'wb')
                ff.write(ss.getvalue())
                ff.close()
                ss.close()

if __name__ == '__main__':
    fetcher = Fetcher()
    url = sys.argv[1]
    fetcher.fetch(url)
