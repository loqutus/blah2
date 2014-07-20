#!/usr/bin/env python3

import os
import sys
import hashlib
import logging
import ipdb

import requests
import tornado.ioloop
import tornado.web
import tornado.httputil

import settings
from settings import TIMEOUT


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
    LOG = settings.LOG1
elif SERVER_ID == '2':
    HOST1 = settings.HOST1
    HOST2 = settings.HOST3
    PORT1 = settings.PORT1
    PORT2 = settings.PORT3
    HOST = settings.HOST2
    PORT = settings.PORT2
    DIR = settings.DIR2
    LOG = settings.LOG2
elif SERVER_ID == '3':
    HOST1 = settings.HOST1
    HOST2 = settings.HOST2
    PORT1 = settings.PORT1
    PORT2 = settings.PORT2
    HOST = settings.HOST3
    PORT = settings.PORT3
    DIR = settings.DIR3
    LOG = settings.LOG3
else:
    logging.debug("Wrong host id, exiting...")
    exit(1)

logging.basicConfig(filename=LOG, level=logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
logging.debug("starting server " + HOST + ":" + str(PORT))


def ask_host(filename, host):
    logging.debug('ask_host')
    if host == 1:
        host = HOST1
        port = PORT1
        logging.debug('ask_HOST1')
    elif host == 2:
        host = HOST2
        port = PORT2
        logging.debug('ask_HOST2')
    url = 'http://' + host + ':' + str(port) + '/info/' + filename
    request_response = requests.get(url, timeout=TIMEOUT)
    logging.debug('request_response: ' + str(request_response.status_code))
    if request_response.status_code == 200:
        return 0
    elif request_response.status_code == 404:
        return 1
    else:
        return 1


def upload(filename, content, md5, host_id):
    logging.debug('upload')
    if host_id == 1:
        host = HOST1
        port = PORT1
    elif host_id == 2:
        host = HOST2
        port = PORT2
    # ipdb.set_trace()
    headers = {'content-type': 'application/bin', 'md5': md5, "client": '0'}
    url_upload = "http://" + host + ":" + str(port) + '/upload/' + filename
    logging.debug('upload: ' + url_upload)
    logging.debug('upload headers: ' + str(headers))
    r = requests.post(url_upload, content, headers=headers, timeout=TIMEOUT)
    logging.debug("upload: " + str(r.status_code))
    if r.status_code == 200:
        logging.debug("upload OK")
    else:
        logging.debug("upload ERROR: " + str(r.status_code))
        exit(1)


def md5sum(filename):
    logging.debug('md5sum')
    with open(filename, "rb") as file:
        data = file.read()
    md5_sum = hashlib.md5(data).hexdigest()
    logging.debug('md5sum: ' + str(md5_sum))
    return md5_sum


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        logging.debug('DownloadHandler')
        with open(DIR + filename, 'rb') as f:
            self.write(f.read())
            f.close()
        logging.debug('file read ok')
        f = open(DIR + filename + '.txt', 'r')
        md5 = f.read()
        logging.debug(filename + '.txt: ' + md5)
        self.set_header('md5', md5)
        logging.debug('DownloadHandlerfinish')
        self.finish()


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        logging.debug('UploadHandler')
        file = DIR + filename
        with open(file, 'wb') as f:
            f.write(self.request.body)
        f.close()
        md5 = self.request.headers.get('md5')
        client = self.request.headers.get('client')
        logging.debug('Client: ' + str(client))
        logging.debug('MD5: ' + md5)
        if md5 == md5sum(file):
            m = open(file + '.txt', 'w')
            m.write(md5)
            logging.debug('ask_host1: ')
            logging.debug('ask_host2: ')
            logging.debug("client: " + str(client))
            if client == '1':
                if ask_host(filename, 1) == 1:
                    logging.debug("upload1")
                    upload(filename, self.request.body, md5, 1)
                    logging.debug("upload1_finish")
                if ask_host(filename, 2) == 1:
                    logging.debug("upload2")
                    upload(filename, self.request.body, md5, 2)
                    logging.debug("upload2_finish")
            self.set_status(200, 'OK')
        else:
            os.remove(file)
            self.set_status(500, 'md5 mismatch')
        self.finish()


class InfoHandler(tornado.web.RequestHandler):
    def get(self, filename):
        logging.debug('InfoHandler')
        filepath = DIR + filename
        if os.path.isfile(filepath):
            isfile = 1
            file_txt = open(filepath + ".txt", 'r')
            file_txt_read = file_txt.read()
            if file_txt_read == md5sum(filepath):
                md5_correct = 1
            else:
                md5_correct = 0
        else:
            isfile = 0
        if isfile == 1 and md5_correct == 1:
            self.write('ISFILE: ' + str(isfile) + ' NAME: ' + \
                       filename + ' MD5: ' + file_txt_read)
            self.set_status(200, 'OK')
        else:
            self.write(filename + 'file not found')
            self.set_status(404, 'file not found')
        self.finish()


class StopHandler(tornado.web.RequestHandler):
    def get(self):
        logging.debug('exiting...')
        tornado.ioloop.IOLoop.instance().stop()


application = tornado.web.Application([
    (r"/download/(.*)", DownloadHandler),
    (r"/upload/(.*)", UploadHandler),
    (r"/info/(.*)", InfoHandler),
    (r"/stop/", StopHandler)
])

if __name__ == '__main__':
    logging.debug('main starting...')
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
    logging.debug('main finished')