
import converters
import parsers
import datetime


#  Epoch time in UTC.
def now_milliseconds():
    return converters.datetime_to_milliseconds(now_datetime())

# UTC time as a Datetime object
def now_datetime():
    # ensure we are using millisecond precision.
    dt =  datetime.datetime.utcnow()
    ms = dt.microsecond / 1000 * 1000
    return dt.replace(microsecond=ms)

def now_microseconds():
    '''sorry can't get this precision'''
    return now_milliseconds() * 1000
