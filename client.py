#!/usr/bin/env python3
import sys
import os
import hashlib
import logging
from settings import TIMEOUT, PROJECT_DIR

import requests


ACTION = sys.argv[1]
if ACTION != 'stop':
    FILE = sys.argv[2]
    FILENAME = os.path.split(FILE)[1]
    HOST = sys.argv[3].split(':')[0]
    PORT = sys.argv[3].split(':')[1]
    URL_DOWNLOAD = 'http://' + HOST + ':' + PORT + '/download/' + FILENAME
    URL_UPLOAD = 'http://' + HOST + ':' + PORT + '/upload/' + FILENAME
    URL_REMOVE = 'http://' + HOST + ':' + PORT + '/remove/' + FILE
    URL_INFO = 'http://' + HOST + ':' + PORT + '/info/' + FILENAME

else:
    HOST = sys.argv[2].split(':')[0]
    PORT = sys.argv[2].split(':')[1]
    URL_STOP = 'http://' + HOST + ':' + PORT + '/stop/'

logging.basicConfig(filename=PROJECT_DIR + 'client.log', level=logging.DEBUG)
logging.debug('client')
logging.debug(sys.argv[2])
def md5():
    logging.debug('md5')
    with open(FILE, 'rb') as file:
        data = file.read()
        md5_sum = hashlib.md5(data).hexdigest()
        logging.debug(md5_sum)
        return md5_sum


def upload():
    logging.debug('upload')
    logging.debug(FILE)
    if os.path.isfile(FILE):
        if info() == 0:
            logging.debug('file exists on server, exiting...')
            return (1)
        data = open(FILE, 'rb').read()
        headers = {'content-type': 'application/bin', 'md5': md5(), 'client': '1'}
        logging.debug('upload file:' + str(FILENAME))
        logging.debug('upload headers:' + str(headers))
        logging.debug('upload_url:' + URL_UPLOAD)
        try:
            r = requests.post(URL_UPLOAD, data, headers=headers, timeout=TIMEOUT)
        except requests.exceptions.Timeout:
            logging.debug('upload timeout, exiting...')
            return (1)
        if r.status_code == 200:
            logging.debug('upload succeeded')
            return (0)
        else:
            logging.debug('ERROR: ' + str(r.status_code))
            return (1)
    else:
        logging.debug('no such file, exiting...')
        return (1)


def info():
    logging.debug('info')
    r = requests.get(URL_INFO, timeout=TIMEOUT)
    #logging.debug(str(r.content.decode('ascii')))

    if r.status_code == 200:
        logging.debug('OK')
        exit(0)
    elif r.status_code == 404:
        logging.debug('ERROR: file not found')
        exit(1)
    elif r.status_code == 500:
        logging.debug('ERROR: server error')
        exit(1)


def download():
    logging.debug('download')
    header = {'client': '1'}
    r = requests.get(URL_DOWNLOAD, headers=header, timeout=TIMEOUT)
    logging.debug(str(r.status_code))
    if r.status_code == 200:
        with open(FILE, 'wb') as f:
            f.write(r.content)
        logging.debug('200')
    else:
        logging.debug('ERROR ' + str(r.status_code))
        exit(1)
    logging.debug('headers: ' + str(r.headers))
    if r.headers['md5'] == md5():
        logging.debug('OK')
        exit(0)

    else:
        logging.debug('md5, exiting...')
        exit(1)


def stop():
    logging.debug('stop')
    try:
        r = requests.get(URL_STOP, timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        logging.debug('server is not running...')
        exit(0)
    except requests.exceptions.Timeout:
        os.system('killall -9 python3 ./server.py')
        exit(0)
    if r.status_code == 200:
        logging.debug('server stopped')
        exit(0)
    else:
        logging.debug('server still running...')
        exit(1)


def remove():
    logging.debug('remove')
    try:
        headers = {'client': '1'}
        r = requests.get(URL_REMOVE, headers=headers, timeout=TIMEOUT)
    except(requests.exceptions.ConnectionError):
        logging.debug('server is not running...')
        exit(0)

    except(requests.exceptions.Timeout):
        logging.debug('server timeout...')
        exit(0)


if __name__ == '__main__':
    logging.debug('main starting')
    if ACTION == 'upload':
        if upload() == 1:
            exit(1)
        else:
            exit(0)
    elif ACTION == 'download':
        download()
    elif ACTION == 'info':
        info()
    elif ACTION == 'stop':
        stop()
    elif ACTION == 'remove':
        remove()
    else:
        logging.debug('unknown action, exiting...')
        exit(1)
    logging.debug('client stopping')
    exit(0)