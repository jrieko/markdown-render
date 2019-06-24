import unittest
import os
from main import main

thisdir = os.path.dirname(os.path.abspath(__file__))

class TestMain(unittest.TestCase):
    def test_main_1(self):
        with open(os.path.join(thisdir, "output1.html")) as outputFile:
            # silly read appends a newline
            expected = outputFile.read().rstrip('\n')
        with open(os.path.join(thisdir, "input1.md")) as inputFile:
            actual = main(inputFile.read())
        self.assertEqual(actual, expected)

    def test_main_2(self):
        with open(os.path.join(thisdir, "output2.html")) as outputFile:
            expected = outputFile.read().rstrip('\n')
        with open(os.path.join(thisdir, "input2.md")) as inputFile:
            actual = main(inputFile.read())
        self.assertEqual(actual, expected)
