smartparse
==========

Makes the ConfigParser smarter.

A SmartParser provides methods to parse options as objects of the datetime-modules, as
list or as 'smartlist'.
Items of a smartlist are automatically tried to converted into different
types (such as: int, float, time, date, datetime).

It also provides additional get- and itme-methods (xget, xitem):
xget tries to get the option as one of the following types (in this
order): int, float, boolean, time, date, datetime, smartlist.
If every type fails the option is given as string.


Latest Version
--------------
The latest version of this project can be found at : http://github.com/thomst/smartparse.


Installation
------------
* Option 1 : Install via pip ::

    pip install smartparse

* Option 2 : If you have downloaded the source ::

    python setup.py install


Documentation
-------------
How to use? ::

    import io
    from smartparse import SmartParser

    CONFIG = """
    [Section]
    bool = yes
    int = 3
    float = 3.3
    time = 23:55:00
    date = 2013.04.24
    datetime = 2013.04.24 23:55:00
    list = one two three four
    smartlist = 3 4.4 1:55 yes 2013.04.24 2013.04.24_01:55
    """

    config = SmartParser(allow_no_value=True)
    config.readfp(io.BytesIO(CONFIG))
    section = dict(self.config.xitems('Section'))

    section['bool']             # True
    section['datetime']         # datetime.datetime(2013, 4, 24, 23, 55)
    section['list']             # ['one', 'two', 'three', 'four']
    section['smartlist'][2]     # datetime.time(1, 55)
    section['smartlist'][4]     # datetime.date(2013, 4, 24)


Reporting Bugs
--------------
Please report bugs at github issue tracker:
https://github.com/thomst/smartparse/issues


Author
------
thomst <thomaslfuss@gmx.de>
Thomas Leichtfuß

* http://github.com/thomst
