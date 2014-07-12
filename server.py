#!/usr/bin/env python3

import os
import sys
import hashlib

import requests
import tornado.ioloop
import tornado.web
import tornado.httputil

import settings


global file_read

SERVER_ID = sys.argv[1]

if SERVER_ID == '1':
    HOST1 = settings.HOST2
    HOST2 = settings.HOST3
    PORT1 = settings.PORT2
    PORT2 = settings.PORT3
    HOST = settings.HOST1
    PORT = settings.PORT1
    DIR = settings.DIR1
elif SERVER_ID == '2':
    HOST1 = settings.HOST1
    HOST2 = settings.HOST3
    PORT1 = settings.PORT1
    PORT2 = settings.PORT3
    HOST = settings.HOST2
    PORT = settings.PORT2
    DIR = settings.DIR2
elif SERVER_ID == '3':
    HOST1 = settings.HOST1
    HOST2 = settings.HOST2
    PORT1 = settings.PORT1
    PORT2 = settings.PORT2
    HOST = settings.HOST3
    PORT = settings.PORT3
    DIR = settings.DIR3
else:
    print("Wrong host id, exiting...")
    exit(1)


def ask_host(filename, host):
    if host == 1:
        host = HOST1
        port = PORT1
    elif host == 2:
        host = HOST2
        port = PORT2
    request_response = requests.get('http://' + host + ':' + str(port) + '/info/' + filename)
    request = request_response.content.decode('ascii')
    print(request.split())
    if request_response.status_code == 200:
        return request.split()[5]
    else:
        return 0


def upload(filename, content, md5, host_id):
    if host_id == 1:
        host = HOST1
        port = PORT1
    elif host_id == 2:
        host = HOST2
        port = PORT2
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
        with open(DIR + filename, 'rb') as f:
            self.write(f.read())
            f.close()
        f = open(DIR + filename + '.txt', 'r')
        md5 = f.read()
        self.set_header('MD5', md5)
        self.finish()


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        file = DIR + filename
        with open(file, 'wb') as f:
            f.write(self.request.body)
        md5 = self.request.headers.get('MD5')
        print(self.request.headers.get('MD5'))
        if md5 == md5sum(file):
            m = open(file + '.txt', 'w')
            m.write(md5)
            # if ask_host(filename, 2) == 0:
            print(ask_host(filename, 1))
            print(ask_host(filename, 2))

            if ask_host(filename, 1) == 0:
                upload(filename, self.request.body, md5, 1)
            if ask_host(filename, 2) == 0:
                upload(filename, self.request.body, md5, 2)
            self.set_status(200, 'OK')
        else:
            os.remove(file)
            self.set_status(500, 'md5 mismatch')
        self.finish()


class InfoHandler(tornado.web.RequestHandler):
    def get(self, filename):
        filepath = DIR + filename
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
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()