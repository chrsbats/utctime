import unittest
from utctime import now_milliseconds, now_datetime 
from utctime.converters import milliseconds_to_datetime, datetime_to_milliseconds

class TestConverters(unittest.TestCase):
    
    def test_millisecond_conversions(self):
        utc = now_milliseconds()
        d = milliseconds_to_datetime(utc)
        assert(utc == datetime_to_milliseconds(d))
        

    def test_datetime_conversions(self): 
        utc = now_datetime()
        d = datetime_to_milliseconds(utc)
        assert(utc == milliseconds_to_datetime(d))



if __name__ == '__main__':
    unittest.main()


