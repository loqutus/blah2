from subprocess import call
import os


class Git:
    def __init__(self, directory='.'):
        self.directory = directory
        if not os.getcwd() == directory:
            os.chdir(directory)

    def cd(self):
        if not os.getcwd() == self.directory:
            os.chdir(self.directory)

    def init(self):
        self.cd()
        r = call('git init', shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git init failed')

    def add(self, filename='*'):
        self.cd()
        r = call('git add ' + filename, shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git add failed')

    def commit(self, message='commit'):
        self.cd()
        r = call("git commit -m \'" + message + "\'", shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git commit failed')

    def push(self, repo='origin', branch='master'):
        self.cd()
        r = call('git push ' + repo + ' ' + branch, shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git push failed')

    def pull(self):
        self.cd()
        r = call('git pull', shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git put failed')

    def clone(self, url):
        self.cd()
        r = call('git clone ' + url, shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git clone failed')

    def rm(self, filename):
        self.cd()
        r = call('git rm ' + filename, shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git rm failed')

    def checkout_to_branch(self, branch='master'):
        self.cd()
        r = call('git checkout ' + branch, shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git checkout failed')

    def checkout_to_commit(self, commit='', files='.'):
        self.cd()
        r = call('git checkout ' + commit + '' + files, shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git checkout failed')

    def branch(self, branch='master'):
        self.cd()
        r = call('git branch ' + branch, shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git branch failed')

    def merge(self, branch='master'):
        self.cd()
        r = call('git merge ' + branch, shell=True)
        if r == 0:
            return 0
        else:
            raise Exception('git merge failed')