# -*- coding: utf-8 -*-


from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging
import os


from yabs.const import KEY_HOSTNAME, KEY_OUT, KEY_PORT, KEY_ROOT


class rq_handler_class(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):

        logging.info(format % args)


def run(context, options=None):

    os.chdir(context[KEY_OUT][KEY_ROOT])

    requesth = rq_handler_class
    requesth.extensions_map.update({".mf": "text/cache-manifest"})

    httpd = HTTPServer((options[KEY_HOSTNAME], options[KEY_PORT]), requesth)

    httpd.serve_forever()
