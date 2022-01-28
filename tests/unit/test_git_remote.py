import unittest
import subprocess
import os
import shutil
import utils

AUTO_GIT_SYNC_ENV_KEY = "AUTO_GIT_SYNC_BRANCH"
IS_UPDATED_SH = "/isUpdated.sh"
BIN_PATH = "/tests/bin"
EXAMPLE_ENV_VAR = "asoneuths"

TEST_DIR_PATH = '/tmp/test_dir'
TEST_SERVER_DIR_PATH = '/tmp/test_server_dir'
TEST_CLIENT_DIR_PATH = '/tmp/test_client_dir'

class TestGitRemoteCheck(unittest.TestCase):

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
        s = utils.GitRepo(TEST_SERVER_DIR_PATH)
        s.init_server_repo()

        c = utils.GitRepo(TEST_CLIENT_DIR_PATH)
        c.init_client_repo()
        c.set_remote(s)
        c.make_branch("aoeu")
        c.initial_commit()
        c.push()

        os.chdir(TEST_DIR_PATH)
        os.environ[AUTO_GIT_SYNC_ENV_KEY] = "aoeu"

        # create our git repo
        out, err = self.exec(['git', 'init'])
        self.assertTrue(out.startswith("Initialized empty Git repository in"))

        # adding remote
        _, err = self.exec(['git', 'remote', 'add', 'origin', TEST_SERVER_DIR_PATH])
        self.assertEqual(err, "")

        # run isUpdated
        out, err = self.exec()
        self.assertEqual(err, "HEAD do not defined")

        # set HEAD
        out, err = self.exec(['git', 'checkout', 'aoeu'])
        print(out)
        self.assertTrue("set up to track remote branch" in out)
        self.assertTrue(err.startswith("Switched to a new branch"))

        # run isUpdated
        out, err = self.exec()
        self.assertEqual(err, "")
        self.assertEqual(out.splitlines()[-1], "Updated.")

if __name__ == '__main__':
    unittest.main()
