#!/usr/bin/env python3

import os
import hashlib

import requests
import tornado.ioloop
import tornado.web
import tornado.httputil

from settings import *


global file_read


def ask_host(filename, host):
    if host == 2:
        host = HOST2
        port = PORT2
    elif host == 3:
        host = HOST3
        port = PORT3
    request_responce = requests.get('http://' + host + ':' + str(port) + '/info/' + filename)
    request = request_responce.content.decode('ascii')
    print(request.split())
    if request_responce.status_code == 200:
        return request.split()[5]
    else:
        return 0


def upload(filename, content, md5, host_id):
    if host_id == 2:
        host = HOST2
        port = PORT2
    elif host_id == 3:
        host = HOST3
        port = PORT3
    headers = {'Content-Type': 'application/bin', 'MD5': md5}
    url_upload = "http://" + host + ":" + str(port) + '/upload/' + filename
    r = requests.post(url_upload, content, headers=headers)
    if r.status_code == 200:
        print("OK")
    else:
        print("ERROR: ", r.status_code)
        exit(1)


def md5sum(filename):
    with open(filename, "rb") as file:
        data = file.read()
        md5_sum = hashlib.md5(data).hexdigest()
        print(md5_sum)
        return md5_sum


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        with open(DIR1 + filename, 'rb') as f:
            self.write(f.read())
            f.close()
        f = open(DIR1 + filename + '.txt', 'r')
        md5 = f.read()
        self.set_header('MD5', md5)
        self.finish()


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        file = DIR1 + filename
        with open(file, 'wb') as f:
            f.write(self.request.body)
        md5 = self.request.headers.get('MD5')
        print(self.request.headers.get('MD5'))
        if md5 == md5sum(file):
            m = open(file + '.txt', 'w')
            m.write(md5)
            # if ask_host(filename, 2) == 0:
            print(ask_host(filename, 2))
            print(ask_host(filename, 3))

            if ask_host(filename, 2) == 0:
                upload(filename, self.request.body, md5, 2)
            if ask_host(filename, 3) == 0:
                upload(filename, self.request.body, md5, 3)
            self.set_status(200, 'OK')
        else:
            os.remove(file)
            self.set_status(500, 'md5 mismatch')
        self.finish()


class InfoHandler(tornado.web.RequestHandler):
    def get(self, filename):
        filepath = DIR1 + filename
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
    application.listen(PORT1)
    tornado.ioloop.IOLoop.instance().start()