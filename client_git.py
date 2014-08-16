#!/usr/bin/env python3
import requests
import sys
import os

ACTION = sys.argv[1]
FILE = sys.argv[2]
FILENAME = os.path.split(FILE)[1]
HOST = sys.argv[3].split(':')[0]
PORT = sys.argv[3].split(':')[1]
URL_UPLOAD = 'http://' + HOST + ':' + PORT + '/upload/' + FILENAME
URL_DOWNLOAD = 'http://' + HOST + ':' + PORT + '/download/' + FILENAME


def upload():
    with open(FILE, 'rb') as f:
        requests.post(URL_UPLOAD, f.read(), timeout=5)
    exit(0)


def download():
    with open(FILENAME, 'wb') as f:
        r = requests.get(URL_DOWNLOAD)
        f.write(r.content)


if __name__ == '__main__':
    if ACTION == 'upload':
        upload()
    elif ACTION == 'download':
        download()
    else:
        print('wrong action, exiting...')
        exit(1)
    exit(0)