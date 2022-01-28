import shutil
import subprocess
import os

def execk(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # print(out.decode('utf-8').rstrip('\n'))
    # print(err.decode('utf-8').rstrip('\n'))


class GitRepo():

    def __init__(self, path):
        self.path = path
        os.mkdir(self.path)
        os.chdir(self.path)
    
    def __del__(self):
        shutil.rmtree(self.path)

    def GetPath(self):
        return self.path
    
    def init_client_repo(self):
        os.chdir(self.path)
        execk("git init")

    def init_server_repo(self):
        os.chdir(self.path)
        execk("git init --bare")

    def set_remote(self, repo):
        os.chdir(self.path)
        execk(f"git remote add origin {repo.GetPath()}")

    def initial_commit(self):
        os.chdir(self.path)
        execk("git config --local user.name Test")
        execk("git config --local user.email test@test.com")
        execk("touch hello.txt")
        execk("git add hello.txt")
        execk("git commit -m test")

    def make_branch(self, str):
        os.chdir(self.path)
        self.actual_branch = str
        execk(f"git checkout -b {str}")
    
    def push(self):
        os.chdir(self.path)
        execk(f"git push -u origin {self.actual_branch}")
