import unittest
from utctime.parsers import from_content, from_url, from_requests_response
import requests


class TestConverters(unittest.TestCase):


    def test_parsers(self):
    

        if True:
            contents = [
                '<p>August 15th, 2013 at 12:00 am</p>',
                '<p>August 15, 2013 at 1:21 am</p>',
                '<p>August 14, 2013, 2:19 PM</p>',
                '<p>AUGUST 14, 2013</p>',
                '<p>August 14, 2013</p>',
                '<p>September 02, 2012</p>',
                '<p>Aug 12, 2008</p>',
                '<p>Aug 09, 2013</p>',
                '<p>May 3rd, 2013</p>',
                # this one won't currently succeed because we don't infer years
                '<p>Tue Aug 13 10:25:38</p>',
                '<p>21 FEB 2012</p>',
                '<p>2013/02/16</p>',
                '<p>2013/02/11 at 9:41 am</p>',
                '<p>16/02/2013</p>',
                '<p>16/02/2013 at 9:41 am</p>',
                '<p class="info" style="display:inline;float:left;">By <a href="mailto:&#99;ra&#105;&#103;&#64;&#114;oc&#107;&#112;&#97;&#112;e&#114;&#115;h&#111;&#116;gu&#110;.&#99;&#111;&#109;">Craig Pearson</a> on May 3rd, 2013 at 9:00 pm.</p>',
            ]

            for content in contents:
                print content
                time = from_content(content)
                print time

        if True:
            urls = [
                'http://www.rockpapershotgun.com/2013/05/03/what-the-cthuck-it-rlyeh-is-a-magrunner-trailer/',
                'http://www.beastsofwar.com/wp-content/uploads/2013/08/Unleashed-Madman1.jpg',
            ]
            for url in urls:
                print url
                time = from_url(url)
                print time

        if True:
            urls = [
                'http://www.rockpapershotgun.com/2013/05/03/what-the-cthuck-it-rlyeh-is-a-magrunner-trailer/',
                'http://www.beastsofwar.com/myth/mercs-minis-prepare-myth-gen-con/',
            ]
            for url in urls:
                response = requests.get(url)
                print url
                time = from_content(response.content)
                print time

        if True:
            urls = [
                'http://www.rockpapershotgun.com/2013/05/03/what-the-cthuck-it-rlyeh-is-a-magrunner-trailer/',
                'http://www.beastsofwar.com/myth/mercs-minis-prepare-myth-gen-con/',
            ]
            for url in urls:
                response = requests.get(url)
                print url
                time = from_requests_response(response)
                print time



if __name__ == '__main__':
    unittest.main()