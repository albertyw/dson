"""
The DSON class converts between python objects and DSON strings
"""

import json
import random
import unittest

class DSON:

    LIST_SPACERS = ['and', 'also']
    OBJECT_SPACERS = [',', '.', '!', '?']

    @staticmethod
    def load(dson):
        """ Main method to convert dson into a python object """
        return NotImplementedError

    @staticmethod
    def dump(obj):
        """ Main method to convert python objects into a DSON string """
        dson = None
        if isinstance(obj, (float, int, long)):
            dson = DSON._dump_number(obj)
        if isinstance(obj, str):
            dson = DSON._dump_string(obj)
        if isinstance(obj, bool):
            dson = DSON._dump_boolean(obj)
        if obj == None:
            dson = DSON._dump_none(obj)
        if isinstance(obj, list):
            dson = DSON._dump_list(obj)
        if isinstance(obj, dict):
            dson = DSON._dump_dict(obj)
        if dson == None:
            raise ValueError("Unserializable value")
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

    @staticmethod
    def _dump_list(obj_list):
        """ Converts python list into DSON strings """
        dson = 'so '
        for i, item in enumerate(obj_list):
            dson += DSON.dump(item)
            if i != len(obj_list) - 1:
                dson += ' ' + random.choice(DSON.LIST_SPACERS)
            dson += ' '
        dson += 'many'
        return dson

    @staticmethod
    def _dump_dict(obj_dict):
        """ Converts python dict into DSON dicts """
        dson = 'such '
        i = 0
        for k, v in obj_dict.items():
            dson += DSON.dump(k)
            dson += ' is '
            dson += DSON.dump(v)
            if i != len(obj_dict) - 1:
                dson += random.choice(DSON.OBJECT_SPACERS)
            dson += ' '
            i += 1
        dson += 'wow'
        return dson


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


class TestList(unittest.TestCase):
    def test_list(self):
        possibilities = []
        possibilities.append('so yes and no many')
        possibilities.append('so yes also no many')
        self.assertTrue(DSON.dump([True, False]) in possibilities)

    def test_variated_list(self):
        possibilities = []
        possibilities.append('so "asdf" and 4 many')
        possibilities.append('so "asdf" also 4 many')
        self.assertTrue(DSON.dump(['asdf', 4]) in possibilities)


class TestDict(unittest.TestCase):
    def test_dict(self):
        expected = 'such "asdf" is yes wow'
        dson = DSON.dump({'asdf': True})
        self.assertEqual(dson, expected)

    def test_large_dict(self):
        import re
        dson = DSON.dump({'asdf': True, 'qwer': 4})
        regex = re.compile('such "qwer" is 4[,\.\!\?] "asdf" is yes wow')
        self.assertTrue(regex.match(dson))


if __name__ == '__main__':
    unittest.main()
