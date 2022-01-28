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
        self.cmd = [os.getcwd() + IS_UPDATED_SH]
        os.environ[AUTO_GIT_SYNC_ENV_KEY] = EXAMPLE_ENV_VAR

    def exec(self, cmd=None):
        if cmd == None:
            cmd = self.cmd
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out.decode('utf-8').rstrip('\n'), err.decode('utf-8').rstrip('\n')

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
        c.init_client_repo()
        c.set_remote(s)
        c.fetch()
        c.checkout(EXAMPLE_ENV_VAR)
        out, err = self.exec()
        self.assertEqual(err, "")
        # self.assertEqual(out.splitlines()[-1], "Updated.")

        cc.new_commit()
        cc.push()
        c.chdir()

        out, err = self.exec()

        self.assertEqual(err, "")
        self.assertEqual(out.splitlines()[-1], "Should update.")


if __name__ == '__main__':
    unittest.main()
