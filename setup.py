from distutils.core import setup

setup(
    name='utctime',
    version='0.1',
    author='C Bates',
    author_email='chrsbats@gmail.com',
    packages=['utctime'],
    scripts=[],
    url='https://github.com/chrsbats/utctime',
    license='LICENSE.TXT',
    description='Getting and converting time in UTC',
    long_description='Converting time in UTC, because time functions in python have a habit of converting to local time.  Also extract meaningful UTC timestamps from web pages.',
    install_requires=[
        "beautifulsoup4==4.3.2",
        "python-dateutil==2.4.2",
        "requests==2.7.0",
    ],
)
