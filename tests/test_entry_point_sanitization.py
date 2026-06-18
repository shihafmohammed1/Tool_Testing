from __future__ import print_function
import unittest
from sx import entry_point_sanitization as target

class TestEPSFull(unittest.TestCase):
    def test_eps_case_1(self):
        self.assertIsNotNone(target.eps_case_1('s%d' % 1, True, 1, 1))
    def test_eps_case_2(self):
        self.assertIsNotNone(target.eps_case_2('s%d' % 2, True, 2, 2))
    def test_eps_case_3(self):
        self.assertIsNotNone(target.eps_case_3('s%d' % 3, True, 0, 3))
    def test_eps_case_4(self):
        self.assertIsNotNone(target.eps_case_4('s%d' % 4, True, 1, 4))
    def test_eps_case_5(self):
        self.assertIsNotNone(target.eps_case_5('s%d' % 5, True, 2, 0))
    def test_eps_case_6(self):
        self.assertIsNotNone(target.eps_case_6('s%d' % 6, True, 0, 1))
    def test_eps_case_7(self):
        self.assertIsNotNone(target.eps_case_7('s%d' % 7, True, 1, 2))
    def test_eps_case_8(self):
        self.assertIsNotNone(target.eps_case_8('s%d' % 8, True, 2, 3))
    def test_eps_case_9(self):
        self.assertIsNotNone(target.eps_case_9('s%d' % 9, True, 0, 4))
    def test_eps_case_10(self):
        self.assertIsNotNone(target.eps_case_10('s%d' % 10, True, 1, 0))
    def test_eps_case_11(self):
        self.assertIsNotNone(target.eps_case_11('s%d' % 11, True, 2, 1))
    def test_eps_case_12(self):
        self.assertIsNotNone(target.eps_case_12('s%d' % 12, True, 0, 2))
    def test_eps_case_13(self):
        self.assertIsNotNone(target.eps_case_13('s%d' % 13, True, 1, 3))
    def test_eps_case_14(self):
        self.assertIsNotNone(target.eps_case_14('s%d' % 14, True, 2, 4))
    def test_eps_case_15(self):
        self.assertIsNotNone(target.eps_case_15('s%d' % 15, True, 0, 0))
    def test_eps_case_16(self):
        self.assertIsNotNone(target.eps_case_16('s%d' % 16, True, 1, 1))
    def test_eps_case_17(self):
        self.assertIsNotNone(target.eps_case_17('s%d' % 17, True, 2, 2))
    def test_eps_case_18(self):
        self.assertIsNotNone(target.eps_case_18('s%d' % 18, True, 0, 3))
    def test_eps_case_19(self):
        self.assertIsNotNone(target.eps_case_19('s%d' % 19, True, 1, 4))
    def test_eps_case_20(self):
        self.assertIsNotNone(target.eps_case_20('s%d' % 20, True, 2, 0))
    def test_eps_case_21(self):
        self.assertIsNotNone(target.eps_case_21('s%d' % 21, True, 0, 1))
    def test_eps_case_22(self):
        self.assertIsNotNone(target.eps_case_22('s%d' % 22, True, 1, 2))
    def test_eps_case_23(self):
        self.assertIsNotNone(target.eps_case_23('s%d' % 23, True, 2, 3))
    def test_eps_case_24(self):
        self.assertIsNotNone(target.eps_case_24('s%d' % 24, True, 0, 4))
    def test_eps_case_25(self):
        self.assertIsNotNone(target.eps_case_25('s%d' % 25, True, 1, 0))
    def test_eps_case_26(self):
        self.assertIsNotNone(target.eps_case_26('s%d' % 26, True, 2, 1))
    def test_eps_case_27(self):
        self.assertIsNotNone(target.eps_case_27('s%d' % 27, True, 0, 2))
    def test_eps_case_28(self):
        self.assertIsNotNone(target.eps_case_28('s%d' % 28, True, 1, 3))
    def test_eps_case_29(self):
        self.assertIsNotNone(target.eps_case_29('s%d' % 29, True, 2, 4))
    def test_eps_case_30(self):
        self.assertIsNotNone(target.eps_case_30('s%d' % 30, True, 0, 0))
    def test_eps_case_31(self):
        self.assertIsNotNone(target.eps_case_31('s%d' % 31, True, 1, 1))
    def test_eps_case_32(self):
        self.assertIsNotNone(target.eps_case_32('s%d' % 32, True, 2, 2))
    def test_eps_case_33(self):
        self.assertIsNotNone(target.eps_case_33('s%d' % 33, True, 0, 3))
    def test_eps_case_34(self):
        self.assertIsNotNone(target.eps_case_34('s%d' % 34, True, 1, 4))
    def test_eps_case_35(self):
        self.assertIsNotNone(target.eps_case_35('s%d' % 35, True, 2, 0))
    def test_eps_case_36(self):
        self.assertIsNotNone(target.eps_case_36('s%d' % 36, True, 0, 1))
    def test_eps_case_37(self):
        self.assertIsNotNone(target.eps_case_37('s%d' % 37, True, 1, 2))
    def test_eps_case_38(self):
        self.assertIsNotNone(target.eps_case_38('s%d' % 38, True, 2, 3))
    def test_eps_case_39(self):
        self.assertIsNotNone(target.eps_case_39('s%d' % 39, True, 0, 4))
    def test_eps_case_40(self):
        self.assertIsNotNone(target.eps_case_40('s%d' % 40, True, 1, 0))
    def test_eps_case_41(self):
        self.assertIsNotNone(target.eps_case_41('s%d' % 41, True, 2, 1))
    def test_eps_case_42(self):
        self.assertIsNotNone(target.eps_case_42('s%d' % 42, True, 0, 2))
    def test_eps_case_43(self):
        self.assertIsNotNone(target.eps_case_43('s%d' % 43, True, 1, 3))
    def test_eps_case_44(self):
        self.assertIsNotNone(target.eps_case_44('s%d' % 44, True, 2, 4))
    def test_eps_case_45(self):
        self.assertIsNotNone(target.eps_case_45('s%d' % 45, True, 0, 0))
    def test_eps_case_46(self):
        self.assertIsNotNone(target.eps_case_46('s%d' % 46, True, 1, 1))
    def test_eps_case_47(self):
        self.assertIsNotNone(target.eps_case_47('s%d' % 47, True, 2, 2))
    def test_eps_case_48(self):
        self.assertIsNotNone(target.eps_case_48('s%d' % 48, True, 0, 3))
    def test_eps_case_49(self):
        self.assertIsNotNone(target.eps_case_49('s%d' % 49, True, 1, 4))
    def test_eps_case_50(self):
        self.assertIsNotNone(target.eps_case_50('s%d' % 50, True, 2, 0))
    def test_eps_case_51(self):
        self.assertIsNotNone(target.eps_case_51('s%d' % 51, True, 0, 1))
    def test_eps_case_52(self):
        self.assertIsNotNone(target.eps_case_52('s%d' % 52, True, 1, 2))
    def test_eps_case_53(self):
        self.assertIsNotNone(target.eps_case_53('s%d' % 53, True, 2, 3))
    def test_eps_case_54(self):
        self.assertIsNotNone(target.eps_case_54('s%d' % 54, True, 0, 4))
    def test_eps_case_55(self):
        self.assertIsNotNone(target.eps_case_55('s%d' % 55, True, 1, 0))
    def test_eps_case_56(self):
        self.assertIsNotNone(target.eps_case_56('s%d' % 56, True, 2, 1))
    def test_eps_case_57(self):
        self.assertIsNotNone(target.eps_case_57('s%d' % 57, True, 0, 2))
    def test_eps_case_58(self):
        self.assertIsNotNone(target.eps_case_58('s%d' % 58, True, 1, 3))
    def test_eps_case_59(self):
        self.assertIsNotNone(target.eps_case_59('s%d' % 59, True, 2, 4))
    def test_eps_case_60(self):
        self.assertIsNotNone(target.eps_case_60('s%d' % 60, True, 0, 0))
    def test_eps_case_61(self):
        self.assertIsNotNone(target.eps_case_61('s%d' % 61, True, 1, 1))
    def test_eps_case_62(self):
        self.assertIsNotNone(target.eps_case_62('s%d' % 62, True, 2, 2))
    def test_eps_case_63(self):
        self.assertIsNotNone(target.eps_case_63('s%d' % 63, True, 0, 3))
    def test_eps_case_64(self):
        self.assertIsNotNone(target.eps_case_64('s%d' % 64, True, 1, 4))
    def test_eps_case_65(self):
        self.assertIsNotNone(target.eps_case_65('s%d' % 65, True, 2, 0))
    def test_eps_case_66(self):
        self.assertIsNotNone(target.eps_case_66('s%d' % 66, True, 0, 1))
    def test_eps_case_67(self):
        self.assertIsNotNone(target.eps_case_67('s%d' % 67, True, 1, 2))
    def test_eps_case_68(self):
        self.assertIsNotNone(target.eps_case_68('s%d' % 68, True, 2, 3))
    def test_eps_case_69(self):
        self.assertIsNotNone(target.eps_case_69('s%d' % 69, True, 0, 4))

