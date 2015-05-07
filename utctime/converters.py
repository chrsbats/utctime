# -*- coding: utf-8 -*-
from __future__ import absolute_import
import calendar
import datetime
import dateutil.tz
import dateutil.parser


def tzinfo(hours=None):
    return dateutil.tz.tzoffset(None, hours*60*60)


def tuple_to_milliseconds(value):
    return calendar.timegm(value) * 1000

def tuple_to_datetime(value):
    return milliseconds_to_datetime(tuple_to_milliseconds(value))

def milliseconds_to_datetime(value):
    value = value / 1000.0
    return datetime.datetime.utcfromtimestamp(value)

def datetime_to_milliseconds(value):
    return calendar.timegm(value.timetuple()) * 1000 + ((value.microsecond) / 1000)

def datetime_to_microseconds(value):
    return datetime_to_milliseconds(value) * 1000

def seconds_to_datetime(value):
    return datetime.datetime.utcfromtimestamp(value)

def datetime_from_isoformat(string):
    d = dateutil.parser.parse(string)
    return d.astimezone(dateutil.tz.tzutc())

def datetime_to_elasticsearch_string(value):
    # 2012-8-27T08:00:30Z
    string = value.strftime('%Y-%m-%dT%H:%M:%SZ')
    return string

