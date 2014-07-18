import sublime, sublime_plugin

import string, random, os.path
import json

# Python 2
try:
    import urllib2
    import httplib

# Python 3
except ImportError:
    import urllib.request as urllib2
    import http.client as httplib

class ScrapfyCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # init an empty unicode string
        content = u''
        # loop over the selections in the view:
        for region in self.view.sel():

            if not region.empty():
                # be sure to insert a newline if we have multiple selections
                if content:
                    content += '\r\n'
                content += self.view.substr(region)

        # if we havent gotten data from selected text,
        # we assume the entire file should be pasted:
        if not content:
            content += self.view.substr(sublime.Region(0, self.view.size()))

        connection = httplib.HTTPConnection("api.scrapfy.io", 80)
        body = {"lang": self.view.settings().get('syntax').split("/")[1].lower(), "content": content}
        connection.request('POST', '/scraps', json.dumps(body), {'Content-Type': 'application/json'})
        response = json.loads(connection.getresponse().read().decode())
        sublime.set_clipboard(response["url"])
        sublime.status_message("SCRAPfy's URL has been copied to your clipboard: " + response["url"])
