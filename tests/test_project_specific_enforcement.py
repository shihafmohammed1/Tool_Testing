from __future__ import print_function
import unittest
from lr.project_specific_enforcement import pse_case_1

class TestBugPartial(unittest.TestCase):
    def test_one_case(self):
        self.assertTrue(pse_case_1('x', True, 1, 3))
