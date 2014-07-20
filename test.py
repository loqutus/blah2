#!/usr/bin/env python3
import os
import glob
import settings
import ipdb
import time


def kill_server():
    """Killing all running servers

    """
    print('kill_server')
    print('killing server 1')
    cmd1 = './client.py stop ' + settings.HOST1 + ':' + str(settings.PORT1)
    print(cmd1)
    os.system(cmd1)
    print('killing server 2')
    cmd2 = './client.py stop ' + settings.HOST2 + ':' + str(settings.PORT2)
    print(cmd2)
    os.system(cmd2)
    print('killing server 3')
    cmd3 = './client.py stop ' + settings.HOST3 + ':' + str(settings.PORT3)
    print(cmd3)
    os.system(cmd3)
    print('all servers killed')


def kill_client():
    """Killing all running clients

    """
    print('kill_client')
    cmd = "for i in $(ps aux | grep client.py | grep -v grep | awk '{print $5}');" + \
          " do kill -9 $i ; done"
    os.system(cmd)
    print('client killed')


def rm_files():
    """Removing existings data files, and logs
    """
    print('rm_files')
    print(os.getcwd())
    for f in glob.glob(os.getcwd() + '/data*/*'):
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
    print("./server.py " + str(server_id) + " &")
    os.system("./server.py " + str(server_id) + " &")


def upload_file(file, host):
    """Uploading test files

    :param file: file to upload
    :param host: host to upload
    """
    print('upload_file')
    if host == 1:
        hostname = settings.HOST1 + ':' + str(settings.PORT1)
    elif host == 2:
        hostname = settings.HOST2 + ':' + str(settings.PORT2)
    elif host == 3:
        hostname = settings.HOST3 + ':' + str(settings.PORT3)
    print("./client.py upload " + str(file) + ".bin " + hostname)
    os.system("./client.py upload " + str(file) + ".bin " + hostname)


if __name__ == '__main__':
    print('main')
    kill_client()
    kill_server()
    rm_files()
    start_server(1)
    start_server(2)
    start_server(3)
    time.sleep(2)
    upload_file(1, 1)
    upload_file(2, 2)
    upload_file(3, 3)
    print('exiting...')