#!/usr/bin/env python3

import tornado.ioloop
import tornado.web

DownloadDir = '/home/rusik/PycharmProjects/blah/data/'


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        with open(DownloadDir + filename, 'rb') as f:
            self.write(f.read())
            f.close()


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.request.body)


application = tornado.web.Application([
    (r"/download/(.*)", DownloadHandler),
    (r"/upload/(.*)", UploadHandler),
])

if __name__ == '__main__':
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()