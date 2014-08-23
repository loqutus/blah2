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
        call('git init', shell=True)
        return 0

    def add(self, filename='*'):
        self.cd()
        call('git add ' + filename, shell=True)
        return 0

    def commit(self, message='commit'):
        self.cd()
        call("git commit -m \'" + message + "\'", shell=True)
        return 0

    def push(self, repo='origin', branch='master'):
        self.cd()
        call('git push ' + repo + ' ' + branch, shell=True)
        return 0

    def pull(self):
        self.cd()
        call('git pull', shell=True)
        return 0

    def clone(self, url):
        self.cd()
        call('git clone ' + url, shell=True)
        return 0

    def rm(self, filename):
        self.cd()
        call('git rm ' + filename, shell=True)
        return 0

    def checkout_to_branch(self, branch='master'):
        self.cd()
        call('git checkout ' + branch, shell=True)
        return 0

    def checkout_to_commit(self, commit='', files='.'):
        self.cd()
        call('git checkout ' + commit + '' + files, shell=True)
        return 0

    def branch(self, branch='master'):
        self.cd()
        call('git branch ' + branch, shell=True)
        return 0

    def merge(self, branch='master'):
        self.cd()
        call('git merge ' + branch, shell=True)
        return 0