#!/usr/bin/env python3

import os
import sys
import hashlib
from logging import debug
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
    debug('Wrong host id, exiting...')
    exit(1)

logging.basicConfig(filename=LOG, level=4)
ch = logging.StreamHandler(sys.stdout)
debug('starting server ' + HOST + ':' + str(PORT))


def ask_host(filename, host):
    debug('ask_host')
    if host == 1:
        host = HOST1
        port = PORT1
        debug('ask_HOST1')
    elif host == 2:
        host = HOST2
        port = PORT2
        debug('ask_HOST2')
    url = 'http://' + host + ':' + str(port) + '/info/' + filename
    request_response = requests.get(url, timeout=TIMEOUT)
    debug('request_response: ' + str(request_response.status_code))
    if request_response.status_code == 200:
        return 0
    elif request_response.status_code == 404:
        return 1
    else:
        return 1


def upload(filename, content, md5, host_id):
    debug('upload')
    if host_id == 1:
        host = HOST1
        port = PORT1
    elif host_id == 2:
        host = HOST2
        port = PORT2
    # ipdb.set_trace()
    headers = {'content-type': 'application/bin', 'md5': md5, 'client': '0'}
    url_upload = 'http://' + host + ':' + str(port) + '/upload/' + filename
    debug('upload: ' + url_upload)
    debug('upload headers: ' + str(headers))
    r = requests.post(url_upload, content, headers=headers, timeout=TIMEOUT)
    debug('upload: ' + str(r.status_code))
    if r.status_code == 200:
        debug('upload OK')
    else:
        debug('upload ERROR: ' + str(r.status_code))
        exit(1)


def download(filename, host_id):
    debug('download')
    if host_id == 1:
        host = HOST1
        port = PORT1
    elif host_id == 2:
        host = HOST2
        port = PORT2
    header = {'client': '1'}
    url_download = 'http://' + HOST + ':' + str(PORT) + '/download/' + filename
    r = requests.get(url_download, headers=header, timeout=TIMEOUT)
    debug(r.status_code)
    if r.status_code == 200 and r.headers.get('md5') == hashlib.md5(r.data).hexdigest():
        debug('file downloaded from host' + host + str(port))
        file = DIR + filename
        with open(file, 'wb') as f:
            f.write(r.data)
        f.close()
        return 0
    else:
        debug('downloading ' + filename + ' from host ' + str(host) + ' failed')
        return 1


def md5sum(filename):
    debug('md5sum')
    with open(filename, 'rb') as file:
        data = file.read()
    md5_sum = hashlib.md5(data).hexdigest()
    debug('md5sum: ' + str(md5_sum))
    return md5_sum


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        debug('DownloadHandler')
        if os.path.isfile(DIR + filename):
            f = open(DIR + filename + '.md5', 'r')
            md5 = f.read()
            if md5sum(DIR + filename) == md5:
                with open(DIR + filename, 'rb') as f:
                    self.write(f.read())
                    f.close()
                debug('file read ok')
                self.set_header('md5', md5)
                debug('md5 correct')
                self.set_status(200)
                debug(filename + '.md5: ' + md5 + ' DownloadHandler exit')
                self.finish()
                return 0
            else:
                debug('md5 error')
                debug('asking other HOSTS')
                client = self.request.headers.get('client')
                if client == '1':
                    if ask_host(filename, 1) == 1:
                        if not download(filename, 1):
                            print('file downloaded from host 1')
                            return 0
                    elif ask_host(filename, 1) == 1:
                        if not download(filename, 2):
                            print('file downloaded from host 2')
                            return 0
                    else:
                        debug('cannot find file on all servers...')
                        self.set_status(500)
                        self.finish()
                        return 1
                self.finish()
        else:
            debug('asking other HOSTS')
            client = self.request.headers.get('client')
            if client == '1':
                if ask_host(filename, 1) == 1:
                    download(filename, 1)
                    return 0
                elif ask_host(filename, 1) == 1:
                    download(filename, 2)
                    return 0
                else:
                    debug('cannot find file on all servers...')
                    self.set_status(500)
                    self.finish()
                    return 1
            else:
                debug('not a client, cannot find file')
                self.finish()
                return 1
            debug('DownloadHandler finish')


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        debug('UploadHandler')
        file = DIR + filename
        md5 = self.request.headers.get('md5')
        client = self.request.headers.get('client')
        debug('Client: ' + str(client))
        debug('MD5: ' + md5)

        if os.path.exists(file):
            debug('file exists')
            if md5 == md5sum(file):
                debug('requested file is the same, as uploading.exit...')
                self.finish()
        else:
            with open(file, 'wb') as f:
                f.write(self.request.body)
                f.close()

        if md5 == md5sum(file):
            m = open(file + '.md5', 'w')
            m.write(md5)
            debug('ask_host1: ')
            debug('ask_host2: ')
            debug('client: ' + str(client))
            if client == '1':
                if ask_host(filename, 1) == 1:
                    debug('upload1')
                    upload(filename, self.request.body, md5, 1)
                    debug('upload1_finish')
                if ask_host(filename, 2) == 1:
                    debug('upload2')
                    upload(filename, self.request.body, md5, 2)
                    debug('upload2_finish')
            self.set_status(200, 'OK')
        else:
            os.remove(file)
            self.set_status(500, 'md5 mismatch')
        self.finish()


class RemoveHandler(tornado.web.RequestHandler):
    def get(self, filename):
        debug('RemoveHandler')
        filepath = DIR + filename
        if os.path.isfile(filepath):
            os.remove(filepath)
            debug('REMOVE ' + filepath)
        if os.path.isfile(filepath + '.md5'):
            os.remove(filepath + '.md5')
            debug('REMOVE ' + filepath)
        else:
            self.write(filename + 'file not found')
            self.set_status(404, 'file not found')
        client = self.request.headers.get('client')
        if client == '1':
            URL_REMOVE1 = 'http://' + HOST1 + ':' + str(PORT1) + '/remove/' + filename
            URL_REMOVE2 = 'http://' + HOST2 + ':' + str(PORT2) + '/remove/' + filename
            if ask_host(filename, 1) == 0:
                debug('remove1')
                headers = {'client': '0'}
                r = requests.get(URL_REMOVE1, headers=headers, timeout=TIMEOUT)
            if ask_host(filename, 2) == 0:
                debug('remove2')
                headers = {'client': '0'}
                r = requests.get(URL_REMOVE2, headers=headers, timeout=TIMEOUT)
        self.finish()


class InfoHandler(tornado.web.RequestHandler):
    def get(self, filename):
        debug('InfoHandler')
        filepath = DIR + filename
        debug(filepath)
        if os.path.isfile(filepath):
            isfile = 1
            debug('isfile')
            file_md5 = open(filepath + '.md5', 'r')
            file_md5_data = file_md5.read()
            if file_md5_data == md5sum(filepath):
                self.write('ISFILE: ' + str(isfile) + ' NAME: ' + filename + ' MD5: ' + file_read)
                self.set_status(200, 'OK')
                self.finish()
                return 0
            else:
                self.write('ISFILE: ' + str(isfile) + ' NAME: ' + filename + ' MD5: ' + file_read)
            try:
                self.set_status(500, 'MD5 error')
            except:
                pass
            self.finish()
            return 1
        else:
            debug('not isfile')
            self.set_status(404, 'file not found')
            debug('404')
            self.finish()
            return 1


class StopHandler(tornado.web.RequestHandler):
    def get(self):
        debug('exiting...')
        tornado.ioloop.IOLoop.instance().stop()


application = tornado.web.Application([
    (r'/download/(.*)', DownloadHandler),
    (r'/upload/(.*)', UploadHandler),
    (r'/remove/(.*)', RemoveHandler),
    (r'/info/(.*)', InfoHandler),
    (r'/stop/', StopHandler)

])

if __name__ == '__main__':
    debug('main starting...')
    application.listen(PORT,'0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
    debug('main finished')