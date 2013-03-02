import os
import sys
import sublime, sublime_plugin
from threading import Thread

st3 = (sublime.version()[0] == '3')
# dist_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, dist_dir)
# if st3:

from .subbank import kuaipan
from .subbank import dbank
from .subbank import baidupan

def plugin_loaded():
    pass

# if st3: sublime.set_timeout(plugin_loaded, 0)

class BankLoader(sublime_plugin.TextCommand):

    def is_enabled(self):
        return True

    def is_visible(self):
        return True

    def getobj(self, args=None):
        client = args[0]
        client.load(args[1])
        try:
            client.download(args[2])
        except:
            sublime.error_message("Unable to fetch remote object")
        else:
            sublime.status_message("File downloaded at %s" % args[2])

    def fetch(self, client, url):
        path_prefix = os.path.expanduser('~/Desktop')
        sublime.set_clipboard(url)
        thread = Thread(target = self.getobj, args = ((client, url, path_prefix), ))
        thread.start()

    # def dbank(self, args=None):
    #     client = args[0]
    #     client.load(args[1])
    #     for i in range(len(client.files)):
    #         print(client.getname(i))
    #         print(client.getdownload(i))
    #         print(client.getxunlei(i))

    def run(self, edit):
        window = self.view.window()
        def read_url(url):
            if url[:27] == 'http://www.kuaipan.cn/file/':
                self.fetch(kuaipan.Klient(), url)
            elif url[:20] == 'http://dl.dbank.com/':
                self.fetch(dbank.Klient(), url)
            elif url[:27] == 'http://pan.baidu.com/share/':
                self.fetch(baidupan.Klient(), url)
            else:
                sublime.error_message("Unsupported URL: %s" % url)
        window.show_input_panel('Net Storage URL:', sublime.get_clipboard(), read_url, None, None)
