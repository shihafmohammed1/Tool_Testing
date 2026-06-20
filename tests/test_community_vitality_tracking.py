from __future__ import print_function
import unittest
from dr.community_vitality_tracking import cvt_case_1

class TestBugPartial(unittest.TestCase):
    def test_one_case(self):
        self.assertTrue(cvt_case_1('x', True, 1, 3))
