# Bank Loader #
## download helper for some storage hosting services ##

## Supported Hosts##

1. dbank.com

	- compatible with [dbank.js v2.8.3](http://st1.dbank.com/netdisk/js/custom-link1.js?v=2.8.3)
	- main _decrypt_ component is as below, originally written in js; _$.md5()_ is from jQuery:
	
			if(typeof dbank === "undefined") {
			    var dbank = {}
			}(function() {
			    var b = {};
			    b.code = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
			    b.encode = function(q, s) {
			        s = (typeof s == "undefined") ? false : s;
			        var i, f, d, u, r, n, m, k, l = [],
			            h = "",
			            p, t, o;
			        var g = b.code;
			        t = s ? q.encodeUTF8() : q;
			        p = t.length % 3;
			        if(p > 0) {
			            while(p++ < 3) {
			                h += "=";
			                t += "\0"
			            }
			        }
			        for(p = 0; p < t.length; p += 3) {
			            i = t.charCodeAt(p);
			            f = t.charCodeAt(p + 1);
			            d = t.charCodeAt(p + 2);
			            u = i << 16 | f << 8 | d;
			            r = u >> 18 & 63;
			            n = u >> 12 & 63;
			            m = u >> 6 & 63;
			            k = u & 63;
			            l[p / 3] = g.charAt(r) + g.charAt(n) + g.charAt(m) + g.charAt(k)
			        }
			        o = l.join("");
			        o = o.slice(0, o.length - h.length) + h;
			        return o
			    };
			    b.decode = function(q, g) {
			        g = (typeof g == "undefined") ? false : g;
			        var i, f, e, r, n, l, k, t, m = [],
			            s, p;
			        var h = b.code;
			        p = g ? q.decodeUTF8() : q;
			        for(var o = 0; o < p.length; o += 4) {
			            r = h.indexOf(p.charAt(o));
			            n = h.indexOf(p.charAt(o + 1));
			            l = h.indexOf(p.charAt(o + 2));
			            k = h.indexOf(p.charAt(o + 3));
			            t = r << 18 | n << 12 | l << 6 | k;
			            i = t >>> 16 & 255;
			            f = t >>> 8 & 255;
			            e = t & 255;
			            m[o / 4] = String.fromCharCode(i, f, e);
			            if(k == 64) {
			                m[o / 4] = String.fromCharCode(i, f)
			            }
			            if(l == 64) {
			                m[o / 4] = String.fromCharCode(i)
			            }
			        }
			        s = m.join("");
			        return g ? s.decodeUTF8() : s
			    };
			    dbank.base64 = b
			}());
			if(typeof dbank === "undefined") {
			    var dbank = {}
			}
			dbank.crt = {};
			(function() {
			    var c = function(h, l) {
			        var k = [],
			            e = 0,
			            d, g = "";
			        for(var f = 0; f < 256; f++) {
			            k[f] = f
			        }
			        for(f = 0; f < 256; f++) {
			            e = (e + k[f] + h.charCodeAt(f % h.length)) % 256;
			            d = k[f];
			            k[f] = k[e];
			            k[e] = d
			        }
			        f = 0;
			        e = 0;
			        for(var m = 0; m < l.length; m++) {
			            f = (f + 1) % 256;
			            e = (e + k[f]) % 256;
			            d = k[f];
			            k[f] = k[e];
			            k[e] = d;
			            g += String.fromCharCode(l.charCodeAt(m) ^ k[(k[f] + k[e]) % 256])
			        }
			        return g
			    };
			    var b = function(d, e) {
			        var h = 0,
			            g = "",
			            l = e.length,
			            f = d.length;
			        for(; h < f; h++) {
			            var k = d.charCodeAt(h) ^ e.charCodeAt(h % l);
			            g += String.fromCharCode(k)
			        }
			        return g
			    };
			    dbank.crt.decrypt = function(g, e) {
			        g = dbank.base64.decode(g);
			        var d, f = e.substr(0, 2);
			        switch(f) {
			        case "ea":
			            d = g;
			            break;
			        case "eb":
			            d = b(g, c(e, e));
			            break;
			        case "ed":
			            d = b(g, $.md5(e));
			            break;
			        default:
			            d = g
			        }
			        return d
			    }
			}());


2. kuaipan.com

	- Implementation is simple, since target url is contained in body.
	
