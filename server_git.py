#!/usr/bin/env python3
import tornado.ioloop
import tornado.web
import git
from settings_git import *


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        print(filename + ' upload')
        print(DATA_DIR + filename)
        git.repo(DATA_DIR)
        with open(DATA_DIR + filename, 'wb') as f:
            f.write(self.request.body)
        git.add(DATA_DIR + filename)
        git.commit(filename + ' added')


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        print(filename + ' download')
        print(DATA_DIR + filename)
        with open(DATA_DIR + filename, 'rb') as f:
            self.write(f.read())


if __name__ == '__main__':
    application = tornado.web.Application([
        (r"/upload/(.*)", UploadHandler),
        (r"/download/(.*)", DownloadHandler)
    ])
    print('main starting...')
    application.listen(PORT, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
    print('main finished')