from __future__ import print_function
import unittest
from sx.entry_point_sanitization import eps_case_1

class TestBugPartial(unittest.TestCase):
    def test_one_case(self):
        self.assertTrue(eps_case_1('x', True, 1, 3))
