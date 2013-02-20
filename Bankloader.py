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

def plugin_loaded():
    pass

# if st3: sublime.set_timeout(plugin_loaded, 0)

class BankLoader(sublime_plugin.TextCommand):

    def is_enabled(self):
        return True

    def is_visible(self):
        return True

    def kuaipan(self, args=None):
        client = args[0]
        client.load(args[1])
        try:
            client.download(args[2])
        except:
            sublime.error_message("Unable to fetch remote object")
        else:
            sublime.status_message("File downloaded at %s" % args[2])

    def dbank(self, args=None):
        client = args[0]
        client.load(args[1])
        for i in range(len(client.files)):
            print(client.getname(i))
            print(client.getdownload(i))
            print(client.getxunlei(i))

    def run(self, edit):
        window = self.view.window()
        def read_url(url):
            path_prefix = os.path.expanduser('~/Desktop')
            if url[:27] == 'http://www.kuaipan.cn/file/':
                sublime.set_clipboard(url)
                client = kuaipan.Klient()
                thread = Thread(target=self.kuaipan, args=((client, url, path_prefix),))
                thread.start()
            elif url[:20] == 'http://dl.dbank.com/':
                sublime.set_clipboard(url)
                client = dbank.Klient()
                thread = Thread(target=self.dbank, args=((client, url, path_prefix),))
                thread.start()
            else:
                sublime.error_message("Unsupported URL: %s" % url)
        window.show_input_panel('Net Storage URL:', sublime.get_clipboard(), read_url, None, None)
