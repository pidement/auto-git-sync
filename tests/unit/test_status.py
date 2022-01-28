from doctest import Example
from email.mime import audio
import unittest
import subprocess
import os
import utils

AUTO_GIT_SYNC_ENV_KEY = "AUTO_GIT_SYNC_BRANCH"
IS_UPDATED_SH = "/isUpdated.sh"
BIN_PATH = "/tests/bin"
EXAMPLE_ENV_VAR = "asoneuths"

TEST_DIR_PATH = '/tmp/test_dir'
TEST_SERVER_DIR_PATH = '/tmp/test_server_dir'
TEST_CLIENT_DIR_PATH = '/tmp/test_client_dir'

class TestUpdatedCheck(unittest.TestCase):

    def setUp(self):
        self.original_dir = os.getcwd()
        self.cmd = [os.getcwd() + IS_UPDATED_SH]
        self.original_path = os.environ["PATH"]

    def tearDown(self):
        os.chdir(self.original_dir)
        os.environ["PATH"] = self.original_path

    def exec(self, cmd=None):
        if cmd == None:
            cmd = self.cmd
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out.decode('utf-8').rstrip('\n'), err.decode('utf-8').rstrip('\n'), process.returncode

    def test_without_git(self):
        os.environ["PATH"] = os.getcwd() + BIN_PATH
        os.environ[AUTO_GIT_SYNC_ENV_KEY] = EXAMPLE_ENV_VAR
        out, err, code = self.exec()
        self.assertEqual(err, "git command not found")
        self.assertEqual(out, "")
        self.assertEqual(code, 1)

    def test_update_branch(self):

        s = utils.GitRepo(TEST_SERVER_DIR_PATH)
        s.init_server_repo()

        cc = utils.GitRepo(TEST_CLIENT_DIR_PATH)
        cc.init_client_repo()
        cc.set_remote(s)
        cc.make_branch(EXAMPLE_ENV_VAR)
        cc.initial_commit()
        cc.push()

        c = utils.GitRepo(TEST_DIR_PATH)

        # check without env var
        del os.environ[AUTO_GIT_SYNC_ENV_KEY]
        _, _, code = self.exec()
        self.assertEqual(code, 1)

        os.environ[AUTO_GIT_SYNC_ENV_KEY] = EXAMPLE_ENV_VAR

        # check without repo initialized
        _, _, code = self.exec()
        self.assertEqual(code, 1)

        c.init_client_repo()

        # check without remote
        _, _, code = self.exec()
        self.assertEqual(code, 1)

        c.set_remote(s)

        # check bad branch
        os.environ[AUTO_GIT_SYNC_ENV_KEY] = "badbranch"
        _, _, code = self.exec()
        self.assertEqual(code, 1)

        os.environ[AUTO_GIT_SYNC_ENV_KEY] = EXAMPLE_ENV_VAR

        c.fetch()

        # check for HEAD
        _, _, code = self.exec()
        self.assertEqual(code, 1)

        c.checkout(EXAMPLE_ENV_VAR)

        # check UPDATED
        _, _, code = self.exec()
        self.assertEqual(code, 1)

        cc.new_commit()
        cc.push()
        c.chdir()

        # check SHOULD UPDATE
        _, _, code = self.exec()
        self.assertEqual(code, 0)

        c.pull()

        # check UPDATED
        _, _, code = self.exec()
        self.assertEqual(code, 1)


if __name__ == '__main__':
    unittest.main()
