# UTC Time

Convert your time stamps and stay in UTC.
Grab UTC time from web requests and web pages.


## Motivation

Time in python is a pain point.  Time functions are spread around numerous libraries.  Converting from one format to another can often change the timezone.  This utility library provides a bunch of converters in one spot that ensure the time stays in UTC.

Getting an accurate timestamp from a web page can also be tricky.  This library parses request headers and request content to get a timestamp in UTC if possible.


## Requirements

python 2.7
beautifulsoup 4.3.2
python-dateutil 2.4.2
requests 2.7.0
six 1.9.0

## Status

Work in progress.  


## Examples

Get time and convert

    In [1]: from utctime import now_milliseconds, now_datetime 

    In [2]: from utctime.converters import milliseconds_to_datetime, datetime_to_milliseconds

    In [3]: utc = now_milliseconds()

    In [4]: d = milliseconds_to_datetime(utc)

    In [5]: utc == datetime_to_milliseconds(d)
    Out[5]: True

    In [6]: utc = now_datetime()

    In [7]: d = datetime_to_milliseconds(utc)

    In [8]: utc == milliseconds_to_datetime(d)
    Out[8]: True

Get timestamp from a web page.

    from utctime.parsers import from_content, from_url, from_requests_response
    import requests

    time = from_url(url)
    response = requests.get(url)
    time = from_requests_response(response)
    time = from_content(response.content)

## Authors

Created by [Christopher Bates](https://github.com/chrsbats) and [Adam Griffiths](https://github.com/adamlwgriffiths).

