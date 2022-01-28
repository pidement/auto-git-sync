import unittest
import subprocess
import os
import shutil

AUTO_GIT_SYNC_ENV_KEY = "AUTO_GIT_SYNC_BRANCH"
IS_UPDATED_SH = "/isUpdated.sh"
BIN_PATH = "/tests/bin"
EXAMPLE_ENV_VAR = "asoneuths"

TEST_DIR_PATH = '/tmp/test_dir'
TEST_SERVER_DIR_PATH = '/tmp/test_server_dir'
TEST_CLIENT_DIR_PATH = '/tmp/test_client_dir'

def execk(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # print(out.decode('utf-8').rstrip('\n'))
    # print(err.decode('utf-8').rstrip('\n'))


class TestGitRemoteCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        original_cwd = os.getcwd()

        os.mkdir(TEST_SERVER_DIR_PATH)
        os.chdir(TEST_SERVER_DIR_PATH)
        execk("git init --bare")
        os.mkdir(TEST_CLIENT_DIR_PATH)
        os.chdir(TEST_CLIENT_DIR_PATH)
        execk("git init")
        execk(f"git remote add origin {TEST_SERVER_DIR_PATH}")
        execk("git config --local user.name Test")
        execk("git config --local user.email test@test.com")
        execk("touch hello.txt")
        execk("git add hello.txt")
        execk("git commit -m test")
        execk("git push -u origin master")
        execk("git checkout -b aoeuaoeu")
        execk("git push -u origin aoeuaoeu")

        os.chdir(original_cwd)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_SERVER_DIR_PATH)
        shutil.rmtree(TEST_CLIENT_DIR_PATH)

    def setUp(self):
        self.cmd = [os.getcwd() + IS_UPDATED_SH]
        self.original_cwd = os.getcwd()
        os.environ[AUTO_GIT_SYNC_ENV_KEY] = EXAMPLE_ENV_VAR
        os.mkdir(TEST_DIR_PATH)
        os.chdir(TEST_DIR_PATH)

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(TEST_DIR_PATH, ignore_errors=True)

    def exec(self, cmd=None):
        if cmd == None:
            cmd = self.cmd
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out.decode('utf-8').rstrip('\n'), err.decode('utf-8').rstrip('\n')

    def test_without_remote(self):
        self.exec(['git', 'init'])
        out, err = self.exec()
        self.assertEqual(err, "remote do not defined")

    def test_with_remote(self):
        self.exec(['git', 'init'])
        self.exec(['git', 'remote', 'add', 'origin', TEST_SERVER_DIR_PATH])
        out, err = self.exec()
        self.assertEqual(err, "branch do not exists on remote")

    def test_with_remote_branch(self):
        os.environ[AUTO_GIT_SYNC_ENV_KEY] = "aoeuaoeu"
        self.exec(['git', 'init'])
        self.exec(['git', 'remote', 'add', 'origin', TEST_SERVER_DIR_PATH])
        out, err = self.exec()
        self.assertEqual(err, "")

if __name__ == '__main__':
    unittest.main()
