"""Simple tests to ensure weirdbase conversionts work as planned"""
import unittest
import uuid

from weirdbase import *


class WeirdBaseTests(unittest.TestCase):

    def setUp(self) -> None:
        self.test_int = uuid.uuid4().int

    def test_int2base_standard(self):
        self.assertEqual('C0FFEE', int2base(0xC0FFEE, 16))
        self.assertEqual('-C0FFEE', int2base(0-0xC0FFEE, 16))

    def test_int2base_custom(self):
        chars = '0123456789abcdef'
        self.assertEqual('c0ffee', int2base(0xC0FFEE, 16, chars))
        self.assertEqual('-c0ffee', int2base(0-0xC0FFEE, 16, chars))

    def test_base2int_standard(self):
        self.assertEqual(0xC0FFEE, base2int('C0FFEE', 16))
        self.assertEqual(0-0xC0FFEE, base2int('-C0FFEE', 16))

    def test_base2int_custom(self):
        chars = '0123456789abcdef'
        self.assertEqual(0xC0FFEE, base2int('c0ffee', 16, chars))
        self.assertEqual(0-0xC0FFEE, base2int('-c0ffee', 16, chars))

    def test_2way_conversion(self):
        # can base2int correctly convert values produced by int2base
        testval = int2base(self.test_int, len(DEFAULT_CHARS))
        self.assertEqual(self.test_int, base2int(testval, len(DEFAULT_CHARS)))
        self.assertEqual(0-self.test_int, base2int('-' + testval, len(DEFAULT_CHARS)))  # Negatives work?


if __name__ == '__main__':
    unittest.main()
