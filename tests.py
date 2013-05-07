import unittest
import datetime
import ConfigParser
import io

import smartparse
from smartparse import RawSmartParser
from smartparse import SmartParser
from smartparse import SafeSmartParser


CONFIG = """
[SectionOne]
bool = yes
int = 3
float = 3.3

[SectionTwo]
time = 23:55:00
date = 2013.04.24
datetime = 2013.04.24 23:55:00
list = one two three four
smartlist = 3 4.4 1:55 yes 2013.04.24 2013-04-24_01:55
"""

smartparse.timeparser.ENDIAN.set('big')


class TestMixin:
    def init(self):
        self.config.readfp(io.BytesIO(CONFIG))
        self.section_one = dict(self.config.xitems('SectionOne'))
        self.section_two = dict(self.config.xitems('SectionTwo'))

    def test_raises(self):
        self.assertRaises(ValueError, self.config.gettime, 'SectionTwo', 'date')
        self.assertRaises(ValueError, self.config.getdate, 'SectionTwo', 'time')
        self.assertRaises(ValueError, self.config.getdatetime, 'SectionTwo', 'smartlist')
        self.assertRaises(ValueError, self.config._checklen, [1])

    def test_type(self):
        self.assertIsInstance(self.config.gettime('SectionTwo', 'time'), datetime.time)
        self.assertIsInstance(self.config.getdate('SectionTwo', 'date'), datetime.date)
        self.assertIsInstance(self.config.getdatetime('SectionTwo', 'datetime'), datetime.datetime)
        self.assertIsInstance(self.config.getlist('SectionTwo', 'list'), list)
        self.assertIsInstance(self.config.getsmartlist('SectionTwo', 'smartlist'), list)

        self.assertIsInstance(self.section_one['bool'], bool)
        self.assertIsInstance(self.section_one['int'], int)
        self.assertIsInstance(self.section_one['float'], float)

        self.assertIsInstance(self.section_two['time'], datetime.time)
        self.assertIsInstance(self.section_two['list'], list)
        self.assertIsInstance(self.section_two['smartlist'][0], int)
        self.assertIsInstance(self.section_two['smartlist'][1], float)
        self.assertIsInstance(self.section_two['smartlist'][2], datetime.time)
        self.assertIsInstance(self.section_two['smartlist'][3], str)
        self.assertIsInstance(self.section_two['smartlist'][4], datetime.date)
        self.assertIsInstance(self.section_two['smartlist'][5], datetime.datetime)

    def test_value(self):
        self.assertEqual(self.section_two['time'], datetime.time(23,55))
        self.assertEqual(len(self.section_two['list']), 4)
        self.assertEqual(self.section_two['smartlist'][1], 4.4)
        self.assertEqual(self.section_two['smartlist'][2], datetime.time(1,55))
        self.assertEqual(self.section_two['smartlist'][4], datetime.date(2013, 4, 24))
        self.assertEqual(self.section_two['smartlist'][5], datetime.datetime(2013, 4, 24, 1, 55))


class RawSmartParserTests(unittest.TestCase, TestMixin):
    def setUp(self):
        self.config = RawSmartParser(allow_no_value=True)
        self.init()

class SmartParserTests(unittest.TestCase, TestMixin):
    def setUp(self):
        self.config = SmartParser(allow_no_value=True)
        self.init()

class SaveSmartParserTests(unittest.TestCase, TestMixin):
    def setUp(self):
        self.config = SafeSmartParser(allow_no_value=True)
        self.init()




if __name__ == '__main__':
    unittest.main()
