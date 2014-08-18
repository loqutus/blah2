#!/usr/bin/env python3
import sys
import os
import hashlib
import logging
from logging import debug
from settings import TIMEOUT, PROJECT_DIR

import requests

logging.basicConfig(filename=PROJECT_DIR + 'client.log', level=logging.DEBUG)
debug('client starting')
debug('PROJECT_DIR: ' + PROJECT_DIR)

ACTION = sys.argv[1]
if ACTION != 'stop':
    FILE = sys.argv[2]
    FILENAME = os.path.split(FILE)[1]
    HOST = sys.argv[3].split(':')[0]
    PORT = sys.argv[3].split(':')[1]
    URL_DOWNLOAD = 'http://' + HOST + ':' + PORT + '/download/' + FILENAME
    URL_UPLOAD = 'http://' + HOST + ':' + PORT + '/upload/' + FILENAME
    URL_REMOVE = 'http://' + HOST + ':' + PORT + '/remove/' + FILENAME
    URL_INFO = 'http://' + HOST + ':' + PORT + '/info/' + FILENAME

    debug('FILE: ' + FILE)
    debug('HOST: ' + HOST)
    debug('PORT: ' + PORT)
    debug('URL_DOWNLOAD: ' + URL_DOWNLOAD)
    debug('URL_UPLOAD: ' + URL_UPLOAD)
    debug('URL_REMOVE: ' + URL_REMOVE)
    debug('URL_INFO: ' + URL_INFO)

else:
    HOST = sys.argv[2].split(':')[0]
    PORT = sys.argv[2].split(':')[1]
    URL_STOP = 'http://' + HOST + ':' + PORT + '/stop/'

    debug('HOST: ' + HOST)
    debug('PORT: ' + PORT)
    debug('URL_STOP: ' + URL_STOP)


def md5(filename, block_size=2 ** 20):
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


def upload():
    debug('upload ' + FILE)
    if os.path.isfile(FILE):
        if info() == 0:
            debug('file exists on server, exiting...')
            return 1
        else:
            debug('file is not found on server')
        data = open(FILE, 'rb').read()
        headers = {'content-type': 'application/bin', 'md5': md5(FILE), 'client': '1'}
        debug('upload file: ' + str(FILENAME))
        debug('upload headers :' + str(headers))
        debug('upload_url: ' + URL_UPLOAD)
        try:
            r = requests.post(URL_UPLOAD, data, headers=headers, timeout=TIMEOUT)
        except requests.exceptions.Timeout:
            debug('upload timeout, exiting...')
            return 1
        if r.status_code == 200:
            debug('upload succeeded')
            return 0
        else:
            debug('ERROR: ' + str(r.status_code))
            return 1
    else:
        debug('no such file, exiting...')
        return 1


def info():
    debug('info')
    try:
        r = requests.get(URL_INFO, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        debug('info timeout, exiting...')
        return 1

    if r.status_code == 200:
        debug('OK')
        return 0
    elif r.status_code == 404:
        debug('ERROR: file not found')
        return 1
    elif r.status_code == 500:
        debug('ERROR: server error')
        return 1


def download():
    debug('download')
    header = {'client': '1'}
    try:
        r = requests.get(URL_DOWNLOAD, headers=header, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        debug('download timeout, exiting...')
        exit(1)
    debug(str(r.status_code))
    if r.status_code == 200:
        with open(FILE, 'wb') as f:
            f.write(r.content)
        debug('200')
    else:
        debug('ERROR ' + str(r.status_code))
        exit(1)
    debug('headers: ' + str(r.headers))
    if r.headers['md5'] == md5(FILE):
        debug('OK')
        exit(0)

    else:
        debug('md5, exiting...')
        exit(1)


def stop():
    debug('stop')
    try:
        r = requests.get(URL_STOP, timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        debug('server is not running...')
        exit(0)
    except requests.exceptions.Timeout:
        os.system('killall -9 python3 ./server.py')
        exit(0)
    if r.status_code == 200:
        debug('server stopped')
        exit(0)
    else:
        debug('server still running...')
        exit(1)


def remove():
    debug('remove')
    try:
        headers = {'client': '1'}
        r = requests.get(URL_REMOVE, headers=headers, timeout=TIMEOUT)
    except(requests.exceptions.ConnectionError):
        debug('server is not running...')
        exit(0)

    except(requests.exceptions.Timeout):
        debug('server timeout...')
        exit(0)


if __name__ == '__main__':
    debug('main starting')
    if ACTION == 'upload':
        upload()
    elif ACTION == 'download':
        download()
    elif ACTION == 'info':
        info()
    elif ACTION == 'stop':
        stop()
    elif ACTION == 'remove':
        remove()
    else:
        debug('unknown action, exiting...')
        exit(1)
    debug('client stopping')
    exit(0)