#!/usr/bin/env python2
import tornado.ioloop
import tornado.web
import git
from settings_git import *


class UploadHandler(tornado.web.RequestHandler):
    def post(self, filename):
        data_repo = git.Repo(DATA_DIR)
        with open(DATA_DIR + filename, 'wb') as f:
            f.write(self.request.body)
        data_repo.git.add(DATA_DIR + filename)
        data_repo.git.commit(m=filename + ' added')
        return 0


class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        with open(DATA_DIR + filename, 'rb') as f:
            self.write(f.read())
        return 0


if __name__ == '__main__':
    application = tornado.web.Application([
        (r"/upload/", UploadHandler),
        (r"/download/", DownloadHandler)
    ])
    print 'main starting...'
    application.listen(PORT, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
    print 'main finished'