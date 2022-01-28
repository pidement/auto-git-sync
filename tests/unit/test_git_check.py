from genericpath import exists
import unittest
import subprocess
import os
import shutil

AUTO_GIT_SYNC_ENV_KEY = "AUTO_GIT_SYNC_BRANCH"
IS_UPDATED_SH = "/isUpdated.sh"
BIN_PATH = "/tests/bin"
EXAMPLE_ENV_VAR = "asoneuths"

TEST_DIR_PATH = '/tmp/test_dir'

class TestGitCheck(unittest.TestCase):

    def setUp(self):
        os.environ[AUTO_GIT_SYNC_ENV_KEY] = EXAMPLE_ENV_VAR
        self.original_path = os.environ["PATH"]
        self.original_cwd = os.getcwd()
        self.cmd = [os.getcwd() + IS_UPDATED_SH]

    def tearDown(self):
        os.environ["PATH"] = self.original_path
        os.chdir(self.original_cwd)

    def exec(self, cmd=None):
        if cmd == None:
            cmd = self.cmd
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out.decode('utf-8').rstrip('\n'), err.decode('utf-8').rstrip('\n')

    def test_without_git(self):
        os.environ["PATH"] = os.getcwd() + BIN_PATH
        out, err = self.exec()
        self.assertEqual(err, "git command not found")
        self.assertEqual(out, "")

    def test_no_repo(self):
        try:
            os.mkdir(TEST_DIR_PATH)
        except FileExistsError:
            pass
        os.chdir(TEST_DIR_PATH)
        out, err = self.exec()
        self.assertEqual(err, "git repo not found")
        self.assertEqual(out, "")
        os.chdir('/tmp')
        os.removedirs(TEST_DIR_PATH)

    def test_with_repo(self):
        try:
            os.mkdir(TEST_DIR_PATH)
        except FileExistsError:
            pass
        os.chdir(TEST_DIR_PATH)
        self.exec(['git', 'init'])
        out, err = self.exec()
        self.assertEqual(err, "")
        os.chdir('/tmp')
        shutil.rmtree(TEST_DIR_PATH)

if __name__ == '__main__':
    unittest.main()
