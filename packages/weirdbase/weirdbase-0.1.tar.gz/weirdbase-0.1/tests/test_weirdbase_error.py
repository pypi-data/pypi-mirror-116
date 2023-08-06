import unittest
from weirdbase import *


class WeirdBaseErrors(unittest.TestCase):

    def test_weirdbase_negative_rejection_int2base(self):
        with self.assertRaises(ValueError):
            int2base(-10, 32, allow_negative=False)

    def test_weirdbase_negative_rejection_base2int(self):
        with self.assertRaises(ValueError):
            base2int('-HELLO', 36, allow_negative=False)

        # but this one should pass because '-' is in the charmap
        self.assertEqual(
            4359030,
            base2int('-HELLO', 27, chars='-ABCDEFGHIJKLMNOPQRSTUVWXYZ', allow_negative=False))

    def test_base2int_missing_char(self):
        with self.assertRaises(KeyError):
            base2int('HELLO', 10, chars='0123456789')

    def test_base2int_bad_base(self):
        with self.assertRaises(ValueError):
            base2int('HELLO', len(DEFAULT_CHARS)+1)

    def test_int2base_bad_base(self):
        with self.assertRaises(ValueError):
            int2base(9000, len(DEFAULT_CHARS)+1)

    def test_int2base_not_int(self):
        with self.assertRaises(TypeError):
            int2base('HELLO', 16)


if __name__ == '__main__':
    unittest.main()
