#!/usr/bin/env python3
import sys
import os
import hashlib

import requests


ACTION = sys.argv[1]
FILE = sys.argv[2]
HOST = 'localhost'
PORT = '8080'

URL_DOWNLOAD = 'http://' + HOST + ':' + PORT + '/download/' + FILE
URL_UPLOAD = 'http://' + HOST + ':' + PORT + '/upload/' + FILE
URL_INFO = 'http://' + HOST + ':' + PORT + '/info/' + FILE


def md5():
    with open(FILE, "rb") as file:
        data = file.read()
        md5_sum = hashlib.md5(data).hexdigest()
        print(md5_sum)
        return md5_sum


def upload():
    if os.path.isfile(FILE):
        data = open(FILE, "rb").read()
        headers = {'Content-Type': 'application/bin', 'MD5': md5()}
        r = requests.post(URL_UPLOAD, data, headers=headers)
        if r.status_code == 200:
            print("OK")
        else:
            print("ERROR: ", r.status_code)
    else:
        print("no such file, exiting...")
        exit(1)


def info():
    r = requests.get(URL_INFO)
    if r.status_code == 200:
        print("OK")
    else:
        print("ERROR: ", r.status_code)


def download():
    r = requests.get(URL_DOWNLOAD)
    if r.status_code == '200':
        with open(FILE, 'wb') as f:
            for chunk in r.content(4096):
                f.write(chunk)
    else:
        print("server error, exiting...")
        exit(1)


if __name__ == '__main__':
    if ACTION == 'upload':
        upload()
    elif ACTION == 'download':
        download()
    elif ACTION == 'info':
        info()
    else:
        print("unknown action, exiting...")
        exit(1)

