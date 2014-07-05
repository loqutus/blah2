#!/usr/bin/env python3

import os
import hashlib

import tornado.ioloop
import tornado.web


Dir = '/home/rusik/PycharmProjects/blah/data/'


def md5sum(filename):
    with open(filename, "rb") as file:
        data = file.read()
        md5_sum = hashlib.md5(data).hexdigest()
        print(md5_sum)
        return md5_sum


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        with open(Dir + filename, 'rb') as f:
            self.write(f.read())
            f.close()
        self.finish()


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        file = Dir + filename
        with open(file, 'wb') as f:
            f.write(self.request.body)
        md5 = self.request.headers.get('MD5')
        print(self.request.headers.get('MD5'))
        if md5 == md5sum(file):
            m = open(file + '.txt', 'w')
            m.write(md5)
            self.set_status(200, 'OK')
        else:
            os.remove(file)
            self.set_status(500, 'md5 mismatch')
        self.finish()


class InfoHandler(tornado.web.RequestHandler):
    def get(self, filename):
        if os.path.isfile(Dir + filename):
            self.write("1")
        else:
            self.write("0")
        self.finish()


application = tornado.web.Application([
    (r"/download/(.*)", DownloadHandler),
    (r"/upload/(.*)", UploadHandler),
    (r"/info/(.*)", InfoHandler)
])

if __name__ == '__main__':
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()