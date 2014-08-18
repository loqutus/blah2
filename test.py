#!/usr/bin/env python3
import os
import glob
from settings import *
import ipdb
import hashlib
from time import sleep


def md5(filename):
    """Calculating md5 sum of a file

    :param filename: name of file
    :return: md5sum of file
    """
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            data = file.read()
            md5_sum = hashlib.md5(data).hexdigest()
            return md5_sum
    else:
        return 1


def kill_server():
    """Killing all running servers

    """
    print('kill_server')
    print('killing server 1')
    os.system('./client.py stop ' + HOST1 + ':' + PORT1)
    print('killing server 2')
    os.system('./client.py stop ' + HOST2 + ':' + PORT2)
    print('killing server 3')
    os.system('./client.py stop ' + HOST3 + ':' + PORT3)
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
    print('rm_files ' + os.getcwd())
    for f in glob.glob(os.getcwd() + '/data*/*'):
        os.remove(f)
    for f in glob.glob(os.getcwd() + '/hash_data*/*'):
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


def upload_file(hostname):
    """Uploading test files

    :param hostname: host to upload
    """
    print('upload_file')
    for file in os.listdir(TEST_FILES_DIR):
        print('./client.py upload ' + TEST_FILES_DIR + str(file) + ' ' + hostname)
        os.system('./client.py upload ' + TEST_FILES_DIR + str(file) + ' ' + hostname)


def download_file(hostname, directory, md5_directory):
    """Downloading test files

    :param hostname: downloading host
    :param directory: checking dir
    :param md5_directory: directory with md5 files
    """
    print('download_file')
    os.chdir(DOWNLOAD_DIR)
    for file in os.listdir(TEST_FILES_DIR):
        # sleep(1)
        print('../client.py download ' + file + ' ' + hostname)
        os.system('../client.py download ' + file + ' ' + hostname)
        file_path = directory + str(file)
        file_txt_path = md5_directory + str(file) + '.md5'
        if os.path.exists(file_txt_path):
            file_txt_path_file = open(file_txt_path, 'r')
            md5_1 = str(file_txt_path_file.read())
        else:
            md5_1 = '0'
        md5_2 = md5(directory + file)
        md5_3 = md5(DOWNLOAD_DIR + file)
        print(file_path)
        if str(md5_1) == str(md5_2) == str(md5_3):
            print('md5 OK')
        else:
            print('md5 in .md5 file: ' + str(md5_1))
            print('md5 of file: ' + str(md5_2))
            print('md5 of downloaded file: ' + str(md5_3))
        if os.path.exists(DOWNLOAD_DIR + file):
            if md5_1 == md5_2 == md5_3:
                print('md5 OK')
            else:
                print('md5 FAILED')
        else:
            print('file is not downloaded')
            # sleep(1)


def remove_file(hostname, directory, filename):
    """Removing test file

    :param filename: removing file
    :param directory: directory to check if file is removed
    :param hostname: removing host
    """
    print('remove_file')
    print('./client.py remove ' + filename + ' ' + hostname)
    os.system('../client.py remove ' + filename + ' ' + hostname)
    if not os.path.isfile(directory + filename) and \
            not os.path.isfile(directory + filename):
        print('file removed')
        return 0
    else:
        print('file is NOT removed')
        return 1


def rm_file_from_fs(file, directory, md5_directory=''):
    """Removing file from filesystem

    :param file: file to remove
    :param directory: directory with files
    :param md5_directory: directory with md5 files
    """
    print('rm_file ' + directory + file)
    file_path = directory + file
    if os.path.exists(file_path):
        os.remove(file_path)
    if md5_directory == '':
        file_txt_path = md5_directory + file + '.md5'
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
    sleep(2)
    upload_file(HOST1 + ':' + PORT1)
    upload_file(HOST2 + ':' + PORT2)
    upload_file(HOST3 + ':' + PORT3)
    rm_file_from_fs('1', DIR1, HASH_DIR1)
    download_file(HOST1 + ':' + PORT1, DIR1, HASH_DIR1)
    download_file(HOST1 + ':' + PORT2, DIR2, HASH_DIR2)
    download_file(HOST1 + ':' + PORT3, DIR3, HASH_DIR3)
    rm_file_from_fs('1', DIR1, HASH_DIR1)
    rm_file_from_fs('1', DIR2, HASH_DIR2)
    rm_file_from_fs('1', DIR3, HASH_DIR3)
    rm_file_from_fs('1', DOWNLOAD_DIR)
    download_file(HOST1 + ':' + PORT1, DIR1, HASH_DIR1)
    download_file(HOST1 + ':' + PORT2, DIR2, HASH_DIR2)
    download_file(HOST1 + ':' + PORT3, DIR3, HASH_DIR3)
    remove_file(HOST1 + ':' + PORT2, DIR2, '2')
    remove_file(HOST1 + ':' + PORT3, DIR3, '3')
    print('exiting...')