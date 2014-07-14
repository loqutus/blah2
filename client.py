#!/usr/bin/env python3
import sys
import os
import hashlib
import logging
import socket

import requests


ACTION = sys.argv[1]
if ACTION != 'stop':
    FILE = sys.argv[2]
    HOST = sys.argv[3].split(":")[0]
    PORT = sys.argv[3].split(":")[1]
    URL_DOWNLOAD = 'http://' + HOST + ':' + PORT + '/download/' + FILE
    URL_UPLOAD = 'http://' + HOST + ':' + PORT + '/upload/' + FILE
    URL_INFO = 'http://' + HOST + ':' + PORT + '/info/' + FILE

else:
    HOST = sys.argv[2].split(':')[0]
    PORT = sys.argv[2].split(':')[1]
    URL_STOP = 'http://' + HOST + ':' + PORT + '/stop/'

logging.basicConfig(filename='client.log', level=logging.DEBUG)


def md5():
    with open(FILE, "rb") as file:
        data = file.read()
        md5_sum = hashlib.md5(data).hexdigest()
        logging.debug(md5_sum)
        return md5_sum


def upload():
    if os.path.isfile(FILE):
        if info() == 0:
            logging.debug('file exists on server, exiting...')
            exit(1)
        data = open(FILE, "rb").read()
        headers = {'content-type': 'application/bin', 'md5': md5(), 'CLIENT': '1'}
        logging.debug("upload file:" + str(FILE))
        logging.debug('upload headers:' + str(headers))
        logging.debug('upload_url:' + URL_UPLOAD)
        r = requests.post(URL_UPLOAD, data, headers=headers)
        if r.status_code == 200:
            logging.debug("OK")
            exit(0)
        else:
            logging.debug("ERROR: ", r.status_code)
            exit(1)
    else:
        logging.debug("no such file, exiting...")
        exit(1)


def info():
    r = requests.get(URL_INFO)
    logging.debug(r.content.decode("ascii"))

    if r.status_code == 200:
        if r.status_code == 200:
            logging.debug("OK")
            return 0
        elif r.status_code == 404:
            logging.debug("ERROR: " + "file not found")
            return 1


def download():
    r = requests.get(URL_DOWNLOAD)
    if r.status_code == '200':
        with open(FILE, 'wb') as f:
            for chunk in r.content(4096):
                f.write(chunk)
    else:
        logging.debug("ERROR" + str(r.status_code))
        exit(1)
    logging.debug('headers: ' + str(r.headers))
    if r.headers['md5'] == md5():
        logging.debug("OK")
        exit(0)

    else:
        logging.debug("md5, exiting...")
        exit(1)


def stop():
    try:
        s = socket.socket()
        s.connect(HOST, PORT)
    except Exception:
        logging.debug('server is not running...')
        exit(1)
    r = requests.get(URL_STOP)
    if r.status_code == 200:
        logging.debug('server stopped')
        exit(0)
    else:
        logging.debug('server still running...')
        exit(1)


if __name__ == '__main__':
    if ACTION == 'upload':
        upload()
    elif ACTION == 'download':
        download()
    elif ACTION == 'info':
        info()
    elif ACTION == 'stop':
        stop()
    else:
        logging.debug("unknown action, exiting...")
        exit(1)