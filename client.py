#!/usr/bin/env python3
import sys
import os

import requests


ACTION = sys.argv[1]
FILE = sys.argv[2]
HOST = 'localhost'
PORT = '8080'

URL_DOWNLOAD = 'http://' + HOST + ':' + PORT + '/download/' + FILE
URL_UPLOAD = 'http://' + HOST + ':' + PORT + '/upload/' + FILE


def upload():
    if os.path.isfile(FILE):
        r = requests.post(URL_UPLOAD, data=open(FILE, "rb").read())
        if r.status_code == 200:
            print("OK")

        else:
            print("ERROR: ", r.status_code)
    else:
        print("no such file, exiting...")
        exit(1)


def download():
    r = requests.get(URL_DOWNLOAD)
    if r.status_code == '200':
        with open(FILE, 'wb') as f:
            for chunk in r.content(1024):
                f.write(chunk)
    else:
        print("server error, exiting...")
        exit(1)


if __name__ == '__main__':
    if ACTION == 'upload':
        upload()
    elif ACTION == 'download':
        download()
    else:
        print("unknown action, exiting...")
        exit(1)

