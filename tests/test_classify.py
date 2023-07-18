import unittest
from watchyourself.analysis import classify
from watchyourself.util import Inspect


class TestClassfiy(unittest.TestCase):

    def test_unknow(self):
        inspect = Inspect("test", "test", "test")
        self.assertEqual(classify(inspect), "未知")


if __name__ == '__main__':
    unittest.main()
