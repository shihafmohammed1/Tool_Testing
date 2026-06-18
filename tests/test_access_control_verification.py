from __future__ import print_function
import unittest
from sx.access_control_verification import acv_case_1

class TestBugPartial(unittest.TestCase):
    def test_one_case(self):
        self.assertTrue(acv_case_1('x', True, 1, 3))
