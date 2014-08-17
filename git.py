from subprocess import call
import os


def init():
    call('git init', shell=True)
    return 0

def add(filename='*'):
    call('git add ' + filename, shell=True)
    return 0

def commit(message='commit'):
    call("git commit -m \'" + message + "\'", shell=True)
    return 0

def push(repo='origin', branch='master'):
    call('git push ' + repo + ' ' + branch, shell=True)
    return 0

def pull(self):
    call('git pull', shell=True)
    return 0

def repo(dir):
    os.chdir(dir)
    return 0

def clone(url):
    call('git clone ' + url, shell=True)
    return 0

def rm(filename):
    call('git rm ' + filename, shell=True)
    return 0

def checkout_to_branch(branch='master'):
    call('git checkout ' + branch, shell=True)
    return 0

def checkout_to_commit(commit='', files='.'):
    call('git checkout ' + commit + '' + files, shell=True)
    return 0

def branch(branch='master'):
    call('git branch ' + branch, shell=True)
    return 0

def merge(branch='master'):
    call('git merge ' + branch, shell=True)
    return 0