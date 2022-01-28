import unittest
import subprocess
import os

AUTO_GIT_SYNC_ENV_KEY = "AUTO_GIT_SYNC_BRANCH"
IS_UPDATED_SH = "/isUpdated.sh"
EXAMPLE_ENV_VAR = "asoneuths"
MSG_DEFINED = f"{AUTO_GIT_SYNC_ENV_KEY} value is {EXAMPLE_ENV_VAR}"
MSG_NOT_DEFINED = f"Environment variable {AUTO_GIT_SYNC_ENV_KEY} do not defined."

class TestEnvironmentCheck(unittest.TestCase):
    def exec(self):
        process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out.decode('utf-8').rstrip('\n'), err.decode('utf-8').rstrip('\n')

    def setUp(self):
        if AUTO_GIT_SYNC_ENV_KEY in os.environ:
            del os.environ[AUTO_GIT_SYNC_ENV_KEY]

        self.cmd = [os.getcwd() + IS_UPDATED_SH]

    def test_defined_env(self):
        os.environ[AUTO_GIT_SYNC_ENV_KEY] = EXAMPLE_ENV_VAR
        out, error = self.exec()
        self.assertEqual(out.split('\n')[0], MSG_DEFINED)

    def test_not_defined_env(self):
        out, error = self.exec()
        self.assertEqual(error, MSG_NOT_DEFINED)
        self.assertEqual(out, "")

if __name__ == '__main__':
    unittest.main()
