import random
import time
from calendar import calendar
from datetime import datetime, timedelta

import exrex

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def date_time_between(start, end):
    return str_time_prop(start, end, '%Y-%m-%dT%H:%M:%S', random.random())


def date_between(start, end):
    return str_time_prop(start, end, '%Y-%m-%d', random.random())


def hours_period_time_between(hours, start, end):
    rand_date = date_between(start, end)
    return hours_period_time(hours, rand_date)


def hours_period_time(hours, rand_date):
    rand_dt = "{0}T{1}".format(
        rand_date
        , exrex.getone('(2[0-3]|1[0-9]|0[1-9]):[0-5][0-9]:[0-5][0-9]'))

    start_date = datetime.strptime(rand_dt, '%Y-%m-%dT%H:%M:%S')
    end_date = start_date + timedelta(hours=random.randint(0, hours),
                                      minutes=random.randint(0, 59),
                                      seconds=random.randint(0, 59))
    return start_date, end_date
