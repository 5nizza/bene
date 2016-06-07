from peewee import IntegerField
from typing import Iterable
from field_desc import FieldDesc


def extract_adhoc_data(log_str, adhoc_fields:Iterable[FieldDesc]) -> dict:
    """ :return: dict{field name -> typed field value} """

    value_by_name = dict()
    for f_desc in adhoc_fields:
        match = f_desc.compiled_reg_exp.search(log_str)

        value = None
        if match and match.groups():
            assert len(match.groups()) == 1, 'field = %s, len = %i' % (f_desc.name, len(match.groups()))
            value = f_desc.python_type(match.groups()[0])

        value_by_name[f_desc.name] = value

    return value_by_name


##################################################################################
import unittest
import re


class Test(unittest.TestCase):
    def test_extract_adhoc_data_main(self):
        adhoc_fields = (FieldDesc('fate', int, IntegerField(),
                                  re.compile('calculation of fate \(sec\): ([0-9]+)')),
                        FieldDesc('love', int, IntegerField(),
                                  re.compile('calculation of love half-life \(sec\): ([0-9]+)')))
        text = """Some text
        calculation of fate (sec): 123
        hello kitty
        calculation of love half-life (sec): 321
        """
        result = extract_adhoc_data(text, adhoc_fields)
        self.assertDictEqual(result, {'fate':123, 'love':321})

    def test_extract_adhoc_data_corner(self):
        adhoc_fields = (FieldDesc('fate', int, IntegerField(),
                                  re.compile('calculation of fate \(sec\): ([0-9]+)')),
                        FieldDesc('love', int, IntegerField(),
                                  re.compile('calculation of love half-life \(sec\): ([0-9]+)')))
        text = """Some text
        Some other case
        """
        result = extract_adhoc_data(text, adhoc_fields)
        self.assertDictEqual(result, {'fate':None, 'love':None})
