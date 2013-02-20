#!/usr/bin/env python

import hashlib

class DBDecoder():
    __code = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        
    def decode(self, string):
        m = []
        i = 0
        while i < len(string):
            r = self.__code.find(string[i])
            n = self.__code.find(string[i+1])
            l = self.__code.find(string[i+2])
            k = self.__code.find(string[i+3])
            t = r << 18 | n << 12 | l << 6 | k;
            v = t >> 16 & 255
            f = t >> 8 & 255
            e = t & 255
            chars = chr(v)+chr(f)+chr(e)
            if k == 64:
                chars = chr(v)+chr(f)
            if l == 64:
                chars = chr(v)
            # print chars
            m.append(chars)
            i += 4
        return ''.join(m)

    def __c(self, h, l):
        k = []
        e = 0
        d = ''
        g = ''
        for i in xrange(256):
            k.append(i)
        for i in xrange(256):
            e = (e + k[i] + ord(h[i%len(h)]))
            d = k[i]
            k[i] = k[e]
            k[e] = d
        i = 0
        j = 0
        for m in xrange(len(l)):
            i = (i+1)%256
            j = (j+k[i])%256
            d = k[i]
            k[i] = k[j]
            k[j] = d
            g += chr(ord(l[m]) ^ k[(k[i]+k[j])%256])
        return g

    def __b(self, d, e):
        h = 0
        g = ''
        l = len(e)
        f = len(d)
        while h < f:
            g += chr(ord(d[h]) ^ ord(e[h%l]))
            h += 1
        return g

    def decrypt(self, string, encrypt):
        g = self.decode(string)
        d = None
        f = encrypt[:2]
        if f == 'ea':
            d = g
        elif f == 'eb':
            d = self.__b(g, self.__c(encrypt, encrypt))
        elif f == 'ed':
            m = hashlib.md5()
            m.update(encrypt.encode())
            d = self.__b(g, m.hexdigest())
        else:
            d = g
        return d
