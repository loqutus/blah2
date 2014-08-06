#!/usr/bin/env python3
import os
import glob
from settings import *
import ipdb
import time
import hashlib


def md5(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        md5_sum = hashlib.md5(data).hexdigest()
        return md5_sum


def kill_server():
    """Killing all running servers

    """
    print('kill_server')
    print('killing server 1')
    cmd1 = './client.py stop ' + HOST1 + ':' + str(PORT1)
    print(cmd1)
    os.system(cmd1)
    print('killing server 2')
    cmd2 = './client.py stop ' + HOST2 + ':' + str(PORT2)
    print(cmd2)
    os.system(cmd2)
    print('killing server 3')
    cmd3 = './client.py stop ' + HOST3 + ':' + str(PORT3)
    print(cmd3)
    os.system(cmd3)
    print('all servers killed')


def kill_client():
    """Killing all running clients

    """
    print('kill_client')
    cmd = 'for i in $(ps aux | grep client.py | grep -v grep | awk "{print $5}");' + \
          ' do kill -9 $i ; done'
    os.system(cmd)
    print('client killed')


def rm_files():
    """Removing existings data files, and logs
    """
    print('rm_files')
    print(os.getcwd())
    for f in glob.glob(os.getcwd() + '/data*/*'):
        os.remove(f)
    for f in glob.glob(os.getcwd() + '/download/*'):
        os.remove(f)
    if os.path.isfile('server1.log'):
        os.remove('server1.log')
    if os.path.isfile('server2.log'):
        os.remove('server2.log')
    if os.path.isfile('server3.log'):
         os.remove('server3.log')
    if os.path.isfile('client.log'):
        os.remove('client.log')
    print('files removed')


def start_server(server_id):
    """Starting server

    :param server_id: server id
    """
    print('start_server')
    print('./server.py ' + str(server_id) + ' &')
    os.system('./server.py ' + str(server_id) + ' &')


def upload_file(host):
    """Uploading test files

    :param file: file to upload
    :param host: host to upload
    """
    print('upload_file')
    if host == 1:
        hostname = HOST1 + ':' + str(PORT1)
    elif host == 2:
        hostname = HOST2 + ':' + str(PORT2)
    elif host == 3:
        hostname = HOST3 + ':' + str(PORT3)
    for file in os.listdir(TEST_FILES_DIR):
        print('./client.py upload ' + TEST_FILES_DIR + str(file) + ' ' + hostname)
        os.system('./client.py upload ' + TEST_FILES_DIR + str(file) + ' ' + hostname)


def download_file(host):
    """Downloading test files

    :param file: downloading file
    :param host: downloading host
    """
    if host == 1:
        directory = DIR1
    elif host == 2:
        directory = DIR2
    elif host == 3:
        directory = DIR3
    print('download_file')
    if host == 1:
        hostname = HOST1 + ':' + str(PORT1)
    elif host == 2:
        hostname = HOST2 + ':' + str(PORT2)
    elif host == 3:
        hostname = HOST3 + ':' + str(PORT3)
    os.chdir(DOWNLOAD_DIR)
    for file in os.listdir(TEST_FILES_DIR):
        print('./client.py download ' + str(file) + ' ' + hostname)
        os.system('../client.py download ' + str(file) + ' ' + hostname)
    file_path = directory + str(file)
    file_txt_path = directory + str(file) + '.md5'
    if os.path.exists(file_path) and os.path.exists(file_txt_path):
        if md5(directory + file) == \
                md5(DOWNLOAD_DIR + file):
            print('md5 OK')
        else:
            print('md5 FAILED')
    else:
        print('file is not downloaded')


def remove_file(file, host):
    """Removing test files

    :param file: removing file
    :param host: removing host
    """
    print('remove_file')
    if host == 1:
        hostname = HOST1 + ':' + str(PORT1)
        directory = DIR1
    elif host == 2:
        hostname = HOST2 + ':' + str(PORT2)
        directory = DIR2
    elif host == 3:
        hostname = HOST3 + ':' + str(PORT3)
        directory = DIR3
    print('./client.py remove ' + str(file) + '.bin ' + hostname)
    os.system('../client.py remove ' + str(file) + '.bin ' + hostname)
    if os.path.isfile(directory + str(file) + '.bin') == False \
            and os.path.isfile(directory + str(file) + '.bin.txt') == False:
        print('file removed')
        return 0
    else:
        print('file is NOT removed')
        return 1


def rm_file_from_fs(file, dir_id):
    if dir_id == 1:
        directory = DIR1
    elif dir_id == 2:
        directory = DIR2
    elif dir_id == 3:
        directory = DIR3
    print('rm_file ' + directory + ' ' + str(file) + '.bin')
    file_path = directory + str(file) + '.bin'
    file_txt_path = directory + str(file) + '.bin.txt'
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(file_txt_path):
        os.remove(file_txt_path)


if __name__ == '__main__':
    print('main')
    kill_client()
    kill_server()
    rm_files()
    start_server(1)
    start_server(2)
    start_server(3)
    time.sleep(2)
    upload_file(1)
    #upload_file(2)
    #upload_file(3)
    #rm_file_from_fs(1, 1)
    #download_file(1)
    #download_file(2)
    #download_file(3)
    #remove_file(1, 1)
    #remove_file(2, 2)
    #remove_file(3, 3)
    print('exiting...')