#!/usr/bin/env python3
import os
import glob
import settings


def kill_server():
    CMD1 = './client.py stop ' + settings.HOST1 + ':' + str(settings.PORT1)
    CMD2 = './client.py stop ' + settings.HOST2 + ':' + str(settings.PORT2)
    CMD3 = './client.py stop ' + settings.HOST3 + ':' + str(settings.PORT3)
    os.system(CMD1)
    os.system(CMD2)
    os.system(CMD3)
    print('server killed')


def rm_files():
    for f in glob.glob('/home/rusik/PycharmProjects/data*/*'):
        os.remove(f)
    os.remove('server1.log')
    os.remove('server2.log')
    os.remove('server3.log')
    print('files removed')


def start_server(server_id):
    print("./server.py " + str(server_id) + " &")
    os.system("./server.py " + str(server_id) + " &")


def upload_file(file, host):
    if host == 1:
        hostname = settings.HOST1 + ':' + str(settings.PORT1)
    elif host == 2:
        hostname = settings.HOST2 + ':' + str(settings.PORT2)
    elif host == 3:
        hostname = settings.HOST3 + ':' + str(settings.PORT3)
    print("./client.py upload " + str(file) + ".bin " + hostname)
    os.system("./client.py upload " + str(file) + ".bin " + hostname)


if __name__ == '__main__':
    kill_server()
    rm_files()
    start_server(1)
    start_server(2)
    start_server(3)
    # upload_file(1, 1)