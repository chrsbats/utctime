import re
import datetime
import dateutil.parser
from bs4 import BeautifulSoup

def from_requests_response(response):
    """Attempts to find a date from a response object.

    If a more reliable method can be used, (RSS timestamp) use that
    in preference to this.
    """
    content_date = from_content(response.content)
    url_date = from_url(response.url)
    modified_date = from_headers(response)

    # TODO: compare the dates properly and figure out which one is more accurate
    if content_date:
        return content_date
    if url_date:
        return url_date
    if modified_date:
        return modified_date

def from_headers(response):
    if 'last-modified' in response.headers:
        date = dateutil.parser.parse(response.headers['last-modified'])
        return date
    return None

def from_url(url):
    # allow the year to go +1 incase we're on new years eve
    # and dealing with timezones
    max_year = datetime.date.today().year + 1

    def parse_segments(segments):
        for segment in segments:
            try:
                val = int(segment)
                # years
                if val >= 1980 or val <= max_year:
                    yield val
                    continue
                # months
                if val >= 1 or val <= 31:
                    yield val
                    continue
            except Exception as e:
                continue
            except GeneratorExit:
                break

    segments = url.split('/')
    year, month, day = None, None, None
    parser = parse_segments(segments)

    try:
        # try and extract in year order
        year = parser.next()
        month = parser.next()
        day = parser.next()
    except Exception as e:
        pass

    if year:
        if year < 1980 or year > max_year:
            year = None
    if month:
        if month < 1 or month > 12:
            month = None
    if day:
        if day < 1 or day > 31:
            day = None
    if not day:
        day = 1

    if year and month and day:
        try:
            return datetime.datetime(year, month, day)
        except:
            return None

    return None

def parse_month(month):
    return {
        'jan':          1,
        'january':      1,
        'feb':          2,
        'february':     2,
        'mar':          3,
        'march':        3,
        'apr':          4,
        'april':        4,
        'may':          5,
        'jun':          6,
        'june':         6,
        'jul':          7,
        'july':         7,
        'aug':          8,
        'august':       8,
        'sep':          9,
        'sept':         9,
        'september':    9,
        'oct':          10,
        'october':      10,
        'nov':          11,
        'november':     11,
        'dec':          12,
        'december':     12,
    }[month.lower()]

def from_content(content):
    def calculate_time(hour, minute, second, am_pm):
        try:
            if not hour:
                return None

            hour = int(hour)
            minute = int(minute) if minute else 0
            second = int(second) if second else 0

            # convert to 24hr
            if hour <= 12 and am_pm == 'pm':
                hour += 12

            return datetime.time(hour=hour, minute=minute, second=second)
        except Exception as e:
            return None

    def calculate_date(day, day_name, month, month_name, year):
        try:
            if day:
                day = int(day)
            if month:
                month = int(month)
            elif month_name:
                month = parse_month(month_name)
            if year:
                year = int(year)
            else:
                # if we have no year, we need the day name
                # TODO: infer the year from day + day_name + month
                pass

            return datetime.date(year, month, day)
        except:
            return None

    args = {
        'days':         r'(?P<days>[0-3]?[0-9])',
        'day_names':    r'(?P<day_names>mon(day)?|tue(s|sday)?|wed(nesday)?|thur(s|sday)?|fri(day)?|sat(urday)?|sun(day)?)',
        'months':       r'(?P<months>[0-1]?[0-9])',
        'month_names':  r'(?P<month_names>jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(t)?(ember)?|oct(ober)?|nov(ember)?|dec(ember)?)',
        'years':        r'(?P<years>19[8-9][0-9]|20[0-1][0-9])',
        'hours':        r'(?P<hours>[0-1]?[0-9])',
        'minutes':      r'(?P<minutes>[0-5]?[0-9])',
        'seconds':      r'(?P<seconds>[0-5]?[0-9])',
        'am_pm':        r'(?P<am_pm>am|pm)',
    }

    expressions = [
        # August 15th, 2013 at 12:00 am
        # August 15, 2013 at 1:21 am
        # August 14, 2013, 2:19 PM
        # AUGUST 14, 2013
        # August 14, 2013
        # September 02, 2012
        # Aug 12, 2008
        # Aug 09, 2013
        # May 3rd, 2013
        re.compile(
            r'{month_names}\s+{days}(rd|th|nd)?,?\s+{years}((,?\s+|\s+at\s+){hours}:{minutes}(:{seconds})?\s+{am_pm})?'.format(**args),
            re.IGNORECASE
        ),
        # Tue Aug 13 10:25:38
        re.compile(
            r'{day_names}\s+{month_names}\s+{days}(rd|th|nd)?(,?\s+|\s+at\s+){hours}:{minutes}(:{seconds})?(\s+{am_pm})?'.format(**args),
            re.IGNORECASE
        ),
        # 21 FEB 2012
        re.compile(
            r'{days}\s+{month_names}\s+{years}'.format(**args),
            re.IGNORECASE
        ),
        # 16/02/2013
        # 16/02/2013 at 9:41 am
        re.compile(
            r'{days}/{months}/{years}((,?\s|\sat\s){hours}:{minutes}(:{seconds})?\s?({am_pm})?)?'.format(**args),
            re.IGNORECASE
        ),
        # 2013/02/16
        # 2013/02/11 at 9:41 am
        re.compile(
            r'{years}/{months}/{days}((,?\s|\sat\s){hours}:{minutes}(:{seconds})?\s?({am_pm})?)?'.format(**args),
            re.IGNORECASE
        ),
    ]

    if type(content) != BeautifulSoup:
        soup = BeautifulSoup(content)
    else:
        soup = content
    content = soup.stripped_strings

    for string in content:
        for regexp in expressions:
            match = regexp.search(string)

            if match:
                matches = match.groupdict()

                hour = match.group('hours') if 'hours' in matches else None
                minute = match.group('minutes') if 'minutes' in matches else None
                second = match.group('seconds') if 'seconds' in matches else None
                am_pm = match.group('am_pm') if 'am_pm' in matches else None

                day = match.group('days') if 'days' in matches else None
                day_name = match.group('day_names') if 'day_names' in matches else None
                month = match.group('months') if 'months' in matches else None
                month_name = match.group('month_names') if 'month_names' in matches else None

                year = match.group('years') if 'years' in matches else None

                # parse the time
                time = calculate_time(hour, minute, second, am_pm)
                date = calculate_date(day, day_name, month, month_name, year)

                if date and time:
                    return datetime.datetime.combine(date, time)
                elif date:
                    return datetime.datetime(date.year, date.month, date.day)

    return None
