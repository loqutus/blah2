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

SERVER_ID = sys.argv[1]

if SERVER_ID == '1':
    HOST1 = settings.HOST2
    HOST2 = settings.HOST3
    PORT1 = settings.PORT2
    PORT2 = settings.PORT3
    HASH_DIR1 = settings.HASH_DIR2
    HASH_DIR2 = settings.HASH_DIR3
    HASH_DIR = settings.HASH_DIR1
    HOST = settings.HOST1
    PORT = settings.PORT1
    DIR = settings.DIR1
    LOG = settings.LOG1
elif SERVER_ID == '2':
    HOST1 = settings.HOST1
    HOST2 = settings.HOST3
    PORT1 = settings.PORT1
    PORT2 = settings.PORT3
    HASH_DIR1 = settings.HASH_DIR1
    HASH_DIR2 = settings.HASH_DIR3
    HASH_DIR = settings.HASH_DIR2
    HOST = settings.HOST2
    PORT = settings.PORT2
    DIR = settings.DIR2
    LOG = settings.LOG2
elif SERVER_ID == '3':
    HOST1 = settings.HOST1
    HOST2 = settings.HOST2
    PORT1 = settings.PORT1
    PORT2 = settings.PORT2
    HASH_DIR1 = settings.HASH_DIR1
    HASH_DIR2 = settings.HASH_DIR2
    HASH_DIR = settings.HASH_DIR3
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


class Host:
    def __init__(self, host_id):
        if host_id == '1':
            self.host = HOST1
            self.port = PORT1
        elif host_id == '2':
            self.host = HOST2
            self.port = PORT2


def ask_host(filename, host):
    """Ask host about files

    :param filename: filename to ask
    :param host: host to ask
    :return 0 if ok, 1 if fails
    """
    debug('ask_host')
    host_obj = Host(host)
    url = 'http://' + host_obj.host + ':' + str(host_obj.port) + '/info/' + filename
    request_response = requests.get(url, timeout=settings.TIMEOUT)
    debug('request_response: ' + str(request_response.status_code))
    if request_response.status_code == 200:
        return 0
    elif request_response.status_code == 404:
        return 1
    else:
        return 1


def upload(filename, content, md5, host_id):
    """Upload files to host

    :param filename: filename to upload
    :param content: content of file to upload
    :param md5: md5 of file to upload
    :param host_id: host id to upload
    """
    debug('upload')
    host_obj = Host(host_id)
    headers = {'content-type': 'application/bin', 'md5': md5, 'client': '0'}
    url_upload = 'http://' + host_obj.host + ':' + host_obj.port + '/upload/' + filename
    debug('upload: ' + url_upload)
    debug('upload headers: ' + str(headers))
    r = requests.post(url_upload, content, headers=headers, timeout=settings.TIMEOUT)
    debug('upload: ' + str(r.status_code))
    if r.status_code == 200:
        debug('upload OK')
    else:
        debug('upload ERROR: ' + str(r.status_code))
        exit(1)


def download(filename, host_id):
    """Download file from host

    :param filename: filename to download
    :param host_id: host id to download
    :return: 0 if ok, 1 if fails
    """
    debug('download')
    host_obj = Host(host_id)
    header = {'client': '0'}
    url_download = 'http://' + HOST + ':' + str(PORT) + '/download/' + filename
    try:
        r = requests.get(url_download, headers=header, timeout=settings.TIMEOUT)
    except requests.exceptions.Timeout:
        debug('download timeout')
        return 1
    debug(r.status_code)
    if r.status_code == 200 and r.headers.get('md5') == hashlib.md5(r.data).hexdigest():
        debug('file downloaded from host' + host_obj.host + host_obj.port)
        file = DIR + filename
        with open(file, 'wb') as f:
            f.write(r.data)
        f.close()
        return 0
    else:
        debug('downloading ' + filename + ' from host ' + host_obj.host + ' failed')
        return 1


def md5sum(filename, block_size=2 ** 20):
    """Calculate md5 of file

    :param filename: filename to calculate md5
    :return: md5sum of file
    """
    debug('md5sum')
    with open(filename, 'rb') as file:
        md5 = hashlib.md5()
        while True:
            data = file.read(block_size)
            if not data:
                break
            md5.update(data)
    md5_sum = md5.hexdigest()
    debug('md5sum: ' + str(md5_sum))
    return md5_sum


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        """Handle a '/download/' url

        :param filename: filename get to the client
        """
        debug('DownloadHandler')
        if os.path.isfile(DIR + filename):
            debug('file exists')
            f_md5 = open(HASH_DIR + filename + '.md5', 'r')
            md5 = f_md5.read()
            if md5sum(DIR + filename) == md5:
                with open(DIR + filename, 'rb') as f:
                    self.write(f.read())
                    f.close()
                debug('file read ok')
                self.set_header('md5', md5)
                debug('md5 correct')
                self.set_status(200)
                debug(filename + '.md5: ' + md5)
                debug('DownloadHandler exit')

            else:
                debug('md5 error, asking other HOSTS')
                client = self.request.headers.get('client')
                if client == '1':
                    if ask_host(filename, '1') == 1:
                        if not download(filename, '1'):
                            print('file downloaded from host 1')
                    elif ask_host(filename, '2') == 1:
                        if not download(filename, '2'):
                            print('file downloaded from host 2')
                    else:
                        debug('cannot find file on all servers...')
                        self.set_status(500)

        else:
            debug('file does not exist, asking other HOSTS')
            client = self.request.headers.get('client')
            if client == '1':
                if ask_host(filename, '1') == 1:
                    download(filename, 1)
                elif ask_host(filename, '2') == 1:
                    download(filename, 2)
                else:
                    debug('cannot find file on all servers...')
                    self.set_status(500)

            else:
                debug('not a client, cannot find file')
        debug('DownloadHandler finish')


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        """Handler of /upload/

        :param filename: filename to upload
        """
        debug('UploadHandler')
        file = DIR + filename
        md5_file = HASH_DIR + filename
        md5 = self.request.headers.get('md5')
        client = self.request.headers.get('client')
        debug('Client: ' + str(client))
        debug('MD5: ' + md5)

        if os.path.exists(file):
            debug('file exists')
            if md5 == md5sum(file):
                debug('uploaded file is the same, as existing, exiting...')

        else:
            debug('file does not exists, writing...')
            with open(file, 'wb') as f:
                f.write(self.request.body)

        if md5 == md5sum(file):
            debug('md5 correct')
            m = open(md5_file + '.md5', 'w')
            m.write(md5)
            m.close()
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


class RemoveHandler(tornado.web.RequestHandler):
    def get(self, filename):
        """/remove handler

        :param filename: filename to remove
        """
        debug('RemoveHandler')
        filepath = DIR + filename
        md5_filepath = HASH_DIR + filename + '.md5'
        if os.path.isfile(filepath):
            os.remove(filepath)
            debug('REMOVE ' + filepath)
        if os.path.isfile(md5_filepath):
            os.remove(md5_filepath)
            debug('REMOVE ' + filepath)
        else:
            self.write(filename + 'file not found')
            self.set_status(404, 'file not found')
        client = self.request.headers.get('client')
        if client == '1':
            URL_REMOVE1 = 'http://' + HOST1 + ':' + str(PORT1) + '/remove/' + filename
            URL_REMOVE2 = 'http://' + HOST2 + ':' + str(PORT2) + '/remove/' + filename
            if ask_host(filename, '1') == 0:
                debug('remove1')
                headers = {'client': '0'}
                r = requests.get(URL_REMOVE1, headers=headers, timeout=settings.TIMEOUT)
            if ask_host(filename, '2') == 0:
                debug('remove2')
                headers = {'client': '0'}
                r = requests.get(URL_REMOVE2, headers=headers, timeout=settings.TIMEOUT)


class InfoHandler(tornado.web.RequestHandler):
    def get(self, filename):
        """/info handler

        :param filename: filename to remove
        """
        debug('InfoHandler')
        filepath = DIR + filename
        md5_filepath = HASH_DIR + filename + '.md5'
        debug(filepath)
        if os.path.isfile(filepath):
            debug('isfile')
            file_md5 = open(md5_filepath, 'r')
            file_md5_data = file_md5.read()
            if file_md5_data == md5sum(filepath):
                debug('ok')
                self.write('OK')
                self.set_status(200, 'OK')
            else:
                debug('md5 error')
                self.write('MD5 error')
                try:
                    self.set_status(500, 'MD5 error')
                except:
                    pass
        else:
            debug('not isfile')
            self.set_status(404, 'file not found')
            debug('404')


class StopHandler(tornado.web.RequestHandler):
    def get(self):
        """/stop handler

        """
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
    application.listen(PORT, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
    debug('main finished')