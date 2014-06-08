"""
The DSON class converts between python objects and DSON strings
"""

import json
import unittest

class DSON:
    @staticmethod
    def dump(obj):
        """ Main method to convert python objects into a DSON string """
        if isinstance(obj, (float, int, long)):
            dson = DSON._dump_number(obj)
        if isinstance(obj, str):
            dson = DSON._dump_string(obj)
        if isinstance(obj, bool):
            dson = DSON._dump_boolean(obj)
        if obj == None:
            dson = DSON._dump_none(obj)
        return dson

    @staticmethod
    def _dump_number(obj_num):
        """ Converts python numbers into DSON strings """
        dson = str(obj_num)
        dson = dson.replace('e-', ' very ')
        dson = dson.replace('e+', ' VERY ')
        return dson

    @staticmethod
    def _dump_string(obj_str):
        """ Converts python strings into DSON strings """
        dson = json.dumps(obj_str)
        return dson

    @staticmethod
    def _dump_boolean(obj_bool):
        """ Converts python booleans into DSON strings """
        if obj_bool:
            return 'yes'
        return 'no'

    @staticmethod
    def _dump_none(obj_none):
        """ Converts python None into DSON strings """
        return 'empty'


class TestNumber(unittest.TestCase):
    def test_positive_integer(self):
        self.assertEqual(DSON.dump(42), '42')

    def test_negative_integer(self):
        self.assertEqual(DSON.dump(-42), '-42')

    def test_large_integer(self):
        self.assertEqual(DSON.dump(42e-50), '4.2 very 49')

    def test_small_integer(self):
        self.assertEqual(DSON.dump(42e50), '4.2 VERY 51')

    def test_large_float(self):
        self.assertEqual(DSON.dump(42.2e-24), '4.22 very 23')

    def test_small_float(self):
        self.assertEqual(DSON.dump(12.3e45), '1.23 VERY 46')


class TestString(unittest.TestCase):
    def test_string(self):
        self.assertEqual(DSON.dump('asdf'), '"asdf"')

    def test_special_char_string(self):
        self.assertEqual(DSON.dump("asdf\n"), '"asdf\\n"')


class TestBoolean(unittest.TestCase):
    def test_false(self):
        self.assertEqual(DSON.dump(False), 'no')

    def test_true(self):
        self.assertEqual(DSON.dump(True), 'yes')


class TestNone(unittest.TestCase):
    def test_none(self):
        self.assertEqual(DSON.dump(None), 'empty')


if __name__ == '__main__':
    unittest.main()
