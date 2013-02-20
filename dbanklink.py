#!/usr/bin/env python

import md5

__code = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

def decode(string):
    m = []
    i = 0
    while i < len(string):
        r = __code.find(string[i])
        n = __code.find(string[i+1])
        l = __code.find(string[i+2])
        k = __code.find(string[i+3])
        t = r << 18 | n << 12 | l << 6 | k;
        v = t >> 16 & 255
        f = t >> 8 & 255
        e = t & 255
        chars = unichr(v)+unichr(f)+unichr(e)
        if k == 64:
            chars = unichr(v)+unichr(f)
        if l == 64:
            chars = unichr(v)
        # print chars
        m.append(chars)
        i += 4
    return ''.join(m)

def __c(h, l):
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
        g += unichr(ord(l[m]) ^ k[(k[i]+k[j])%256])
    return g

def __b(d, e):
    h = 0
    g = ''
    l = len(e)
    f = len(d)
    while h < f:
        g += unichr(ord(d[h]) ^ ord(e[h%l]))
        h += 1
    return g

def decrypt(string, encrypt):
    g = decode(string)
    d = None
    f = encrypt[:2]
    if f == 'ea':
        d = g
    elif f == 'eb':
        d = __b(g, __c(encrypt, encrypt))
    elif f == 'ed':
        d = __b(g, md5.new(encrypt).hexdigest())
    else:
        d = g
    return d


if __name__ == '__main__':
    data = 'UUdFQgkXHlBeSxBbWQpbHQYKCUsCXxFaXFhWURlwU0RQVxpzQVtZQV4AElcTSxxyTjEMCxNDB1pUHHpcWlFBHFQHUA1VBVIEWQcCD1cTTUtDDFlVQFhbBQMBBgcOAQEBCBVHDwcLUwcFBlZVHhMKVVBVUVVRAwISWUcKAgIaAwAMHQAFCxYJBRQVWwYeCkdaAVhCEAUNUwQHBwUNDgM='
    print decrypt(data, 'ed28227105')
