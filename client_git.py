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
print('action ' + ACTION)
print('file ' + FILE)
print('filename ' + FILENAME)
print('host ' + HOST)
print('port ' + PORT)
print('url_upload ' + URL_UPLOAD)
print('url_download ' + URL_DOWNLOAD)


def upload():
    print('upload')
    headers = {'content-type': 'application/bin'}
    with open(FILE, 'rb') as f:
        requests.post(URL_UPLOAD, f.read(), headers=headers, timeout=5)
    exit(0)


def download():
    print('download')
    with open(FILENAME, 'wb') as f:
        r = requests.get(URL_DOWNLOAD)
        f.write(r.content)
    exit(1)


if __name__ == '__main__':
    print('main')
    if ACTION == 'upload':
        upload()
    elif ACTION == 'download':
        download()
    else:
        print('wrong action, exiting...')
        exit(1)
    exit(0)