import re
from datetime import datetime
import logging


def time_parms_handler(time_option):
    """
    exception test for input datetime.obj including start_time and end_time, you can inout start_time or endtime option
    you checking, then it will return the function which can check for your input datetime formatting
    :param time_option: str
    :return: function
    """

    def input_time_parms_hadnler(input_time_parms):
        """
        The Regex is to confirm whether or not the input datetime is mapping the expectation.
        :param input_time_parms: str
        """
        time_pattern = re.compile(
            "[1,2][0-9]{1,3}-[0,1][0-9]-[0-3][0-9]T([0-1][0-9]|2[0-4]):([0-5][0-9]|60):([0-5][0-9]|60)Z")
        if not isinstance(input_time_parms, str):
            raise Exception("Please input string datetime format for -e {} option".format(time_option))
        elif not time_pattern.search(input_time_parms):
            raise Exception(
                "Please use correct timestamp ISO8601 formatting etc 2020-03-01T09:11:22Z for -e {} option, etc".format(
                    time_option))

    return input_time_parms_hadnler


def st_et_input_exception_handler(start_time, end_time):
    """
    Exception handling for input start and end time, if end time < start_time it will raise exception, if end_time >
    now, it will also return exception
    :param start_time: datetime.obj
    :param end_time: datetime.obj
    :return: void
    """
    if start_time > end_time:
        raise Exception("start_time is after end_time, please re-enter correct start_time and end_time")
    if end_time > datetime.utcnow():
        raise Exception("end_time is after current time, please re-enter correct end_time")
    else:
        print("Parms validation Pass")
