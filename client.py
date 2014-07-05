#!/usr/bin/env python3
import sys

import requests

ACTION = sys.argv[1]
FILE = sys.argv[2]
HOST = 'localhost'
PORT = '8080'

URL_DOWNLOAD = 'http://' + HOST + ':' + PORT + '/download/' + FILE
URL_UPLOAD = 'http://' + HOST + ':' + PORT + '/upload/' + FILE
if __name__ == '__main__':
    if ACTION == 'upload':
        f = {'file': open(FILE, 'rb')}
        requests.post(URL_UPLOAD, files=f)
    elif ACTION == 'download':
        r = requests.get(URL_DOWNLOAD)
        if r.status_code == '200':
            with open(FILE, 'wb') as f:
                for chunk in r.content(1024):
                    f.write(chunk)
        else:
            print("error")
            exit(1)
