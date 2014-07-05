#!/usr/bin/env python3

import os

import tornado.ioloop
import tornado.web


Dir = '/home/rusik/PycharmProjects/blah/data/'


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        with open(Dir + filename, 'rb') as f:
            self.write(f.read())
            f.close()


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        with open(Dir + filename, 'wb') as f:
            f.write(self.request.body)


class InfoHandler(tornado.web.RequestHandler):
    def get(self, filename):
        if os.path.isfile(Dir + filename):
            self.write("1")
        else:
            self.write("0")


application = tornado.web.Application([
    (r"/download/(.*)", DownloadHandler),
    (r"/upload/(.*)", UploadHandler),
    (r"/info/(.*)", InfoHandler)
])

if __name__ == '__main__':
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()