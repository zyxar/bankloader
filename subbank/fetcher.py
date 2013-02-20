#!/usr/bin/env python

import sublime
from urllib.request import urlopen
from os.path import exists, getsize, basename
from io import BufferedWriter, BytesIO
# import sys

# def status(percent):
#     bar_size = 40
#     percent *= 100.0
#     if percent > 100:
#         percent = 100.0
#     dots = int(bar_size * percent / 100)
#     plus = percent / 100 * bar_size - dots
#     if plus > 0.8:
#         plus = '='
#     elif plus > 0.4:
#         plus = '-'
#     else:
#         plus = ''
#     percent = int(percent)
#     bar = '=' * dots + plus
#     bar = '{0:>3}%[{1:<40}]'.format(percent, bar)
#     sys.stdout.write('\r'+bar)
#     sys.stdout.flush()

class Fetcher():
    block_sz = 64 * 1024
    # def __init__(self, url=None):
    #     self.url = url

    # def fetch(self, url=None): # do not use this func
    #     payload = url or self.url
    #     if payload is not None:
    #         uu = urlopen(payload)
    #         filename = payload.split('/')[-1]
    #         #TODO: extract filename from response header
    #         self.retrieve(uu, filename)
    #         uu.close()

    def retrieve(self, socket, filename, save=True):
        size = int(socket.info().get('content-length'))
        url = socket.geturl()        
        if exists(filename) and getsize(filename) == size:
            sublime.status_message("File %s already exists." % filename)
        else:
            sublime.status_message("Downloading: %s. Bytes: %d" % (basename(filename), size))
            if save:
                ff = open(filename, 'wb')
                ss = BufferedWriter(ff)
            else:
                ss = Buffer()
            dld = 0
            while True:
                buf = socket.read(self.block_sz)
                if not buf:
                    break
                dld += len(buf)
                ss.write(buf)
                sublime.status_message("{0} downloading {1:%}".format(basename(filename), dld*1./size))
            ss.close()
            ff.close()
