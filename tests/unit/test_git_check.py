import unittest
import subprocess
import os

AUTO_GIT_SYNC_ENV_KEY = "AUTO_GIT_SYNC_BRANCH"
IS_UPDATED_SH = "/isUpdated.sh"
BIN_PATH = "/tests/bin"
EXAMPLE_ENV_VAR = "asoneuths"

class TestGitCheck(unittest.TestCase):

    def setUp(self):
        self.original_path = os.environ["PATH"]
        self.cmd = [os.getcwd() + IS_UPDATED_SH]

    def tearDown(self):
        os.environ["PATH"] = self.original_path

    def exec(self):
        process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out.decode('utf-8').rstrip('\n'), err.decode('utf-8').rstrip('\n')

    def test_without_git(self):
        os.environ[AUTO_GIT_SYNC_ENV_KEY] = EXAMPLE_ENV_VAR
        os.environ["PATH"] = os.getcwd() + BIN_PATH
        out, err = self.exec()
        self.assertEqual(err, "git command not found")
        self.assertEqual(out, "")

if __name__ == '__main__':
    unittest.main()
