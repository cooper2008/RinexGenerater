import string
from datetime import datetime
from datetime import timedelta

time_convert_list = [x for x in string.ascii_lowercase[:24]]


def string2datetime(timeformating):
    """
    Transfer String format datetime to datetime object, Curry function, input your transfer formatting and return
    time_convertor function, then you can put you datetime string to complie
    :param timeformating: String: time formatting etc '%Y-%M-%dT%H:%m:%SZ'
    :return: func: convertor function
    """

    def convertor(time_string):
        """
        return function you can input the datetime string to transfer to datetime object
        :param time_string: string: datetime string format etc "2017-12-15T12:34:10Z"
        :return: datetime object
        """
        return datetime.strptime(time_string, timeformating)

    return convertor


def dateimeplus_gap(hours):
    """
    Plus a flexible time range for specify timestamp, Curry function, input your flexible hours you, the specify
    timestamp will become time range
    :param hours: int
    :return: function
    """

    def timer_scope(datetime_obj):
        """
        Input datetime object once return function, and it will return time range base on previous flexible
        hours, etc (date_time - hours, datetime + hours)
        :param datetime_obj: datetime.obj
        :return: set (datetime.obj, datetime.obj)
        """
        return (datetime_obj - timedelta(hours=hours), datetime_obj + timedelta(hours=hours))

    return timer_scope


def datetimetostring(datetime_obj):
    """
    Datetime object input you will get three strings, full year, short year, days of the year. etc 2017-01-03 ->
    2017, 17 , 03
    :param datetime_obj: datetime.obj
    :return: set: (string, string, string)
    """
    return (
        datetime_obj.strftime("%Y"),
        datetime_obj.strftime("%y"),
        datetime_obj.strftime("%j")
    )


def gen_dates(b_date, days):
    """
    Generator which use to generate the datetime obj within a time range, using by get_date_list function
    :param b_date: datetime.obj
    :param days: int: the time range from b_date
    :return: generator(date.obj)
    """
    day = timedelta(days=1)
    for i in range(days):
        yield b_date + day * i


def get_date_list(start_time, end_time, gap=0):
    """
    Get a date list from start_time to end_time, you can add flexible time range as well, if you put
    value in gap, such as 2 hours, then start will advance 2 hours, also end will postpone 2 hours
    :param start_time: datetime.obj
    :param end_time: datetime.obj
    :param gap: int
    :return: list(datetime.ojb)
    """
    datetime_plus = dateimeplus_gap(int(gap))
    data = []
    for d in gen_dates(start_time, (
            end_time.replace(hour=0, minute=0, second=0) - start_time.replace(hour=0, minute=0, second=0)).days):
        data.append(d)
    if not data:
        start_time, _ = datetime_plus(start_time)
        _, end_time = datetime_plus(end_time)
        return [start_time, end_time]
    else:
        data.pop(0)
        data.insert(0, start_time)
        data.append(end_time)
        return data


def timetransfergpsinday(start_time=None, end_time=None):
    """
    Convert the hours to gps time represent formatting, Timestamp 0-24 -> a-x
    :param start_time: datetime.obj
    :param end_time: datetime.obj
    :return: list[string]
    """
    if start_time:
        if not end_time:
            return [time_convert_list[num] for num in range(int(start_time.strftime("%H")), 24)]
        else:
            return [time_convert_list[num] for num in
                    range(int(start_time.strftime("%H")), int(end_time.strftime("%H")) + 1)]
    elif end_time:
        return [time_convert_list[num] for num in range(int(end_time.strftime("%H")) + 1)]
    else:
        raise Exception("start_time and end_time can't be set Both None Type")
