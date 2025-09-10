import unittest
from utils.file_utils import file_exists

class TestUtils(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(file_exists(__file__))

if __name__ == "__main__":
    unittest.main()
