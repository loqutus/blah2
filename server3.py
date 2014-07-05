#!/usr/bin/env python3

import os
import hashlib

import tornado.ioloop
import tornado.web
import tornado.httputil

from settings import *


global file_read


def md5sum(filename):
    with open(filename, "rb") as file:
        data = file.read()
        md5_sum = hashlib.md5(data).hexdigest()
        print(md5_sum)
        return md5_sum


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        with open(DIR3 + filename, 'rb') as f:
            self.write(f.read())
            f.close()
        self.finish()


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        file = DIR3 + filename
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
        filepath = DIR3 + filename
        if os.path.isfile(filepath):
            isfile = '1'
            file_txt = open(filepath + ".txt", 'r')
            file_read = file_txt.read()
            if file_read == md5sum(filepath):
                md5_correct = '1'
            else:
                md5_correct = '0'
        else:
            isfile = '0'
        if isfile == '1' and md5_correct == '1':
            self.write('ISFILE: ' + str(isfile) + ' NAME: ' + filename + ' MD5: ' + file_read)
            self.set_status(200, 'OK')
        else:
            self.write('ISFILE: ' + str(isfile))
            self.set_status(500, 'server error')
        self.finish()


application = tornado.web.Application([
    (r"/download/(.*)", DownloadHandler),
    (r"/upload/(.*)", UploadHandler),
    (r"/info/(.*)", InfoHandler)
])

if __name__ == '__main__':
    application.listen(PORT3)
    tornado.ioloop.IOLoop.instance().start()