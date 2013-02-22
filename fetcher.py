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

def savefile(name, stream):
    ff = open(name, 'wb')
    ff.write(stream)
    ff.close()

class Fetcher():
    block_sz = 32 * 1024
    def __init__(self, url=None):
        self.url = url

    def fetch(self, url=None):
        payload = url or self.url
        if payload is not None:
            uu = urlopen(payload)
            filename = payload.split('/')[-1]
            #TODO: extract filename from response header
            self.retrieve(uu, filename)
            uu.close()

    def retrieve(self, socket, filename):
        size = int(socket.info().getheader('content-length'))
        if exists(filename) and getsize(filename) == size:
            try:
                print "File %s already exists." % filename
            except UnicodeEncodeError:
                print "File %s already exists." % filename.encode('UTF-8')
        else:
            try:
                print "Downloading: %s. Bytes: %d" % (filename, size)
            except UnicodeEncodeError:
                print "Downloading: %s. Bytes: %d" % (filename.encode('UTF-8'), size)
            ss = StringIO()
            dld = 0
            while True:
                buf = socket.read(self.block_sz)
                if not buf:
                    break
                dld += len(buf)
                ss.write(buf)
                status(dld*1./size)
            print
            savefile(filename, ss.getvalue())
            ss.close()

if __name__ == '__main__':
    fetcher = Fetcher()
    url = sys.argv[1]
    fetcher.fetch(url)
