import timer_convertor
import logging

# ftp://www.ngs.noaa.gov/cors/rinex/2017/257/nybp/nybp257x.17o.gz
DEFAULT_URL = '/cors/rinex'


def link_generator(year_str, day_str, station_id, repr_time_charactor, year_short_str):
    """
    Combine the information to become a ftp dir link, include station_id, year, days of the year
    etc /cors/rinex/2017/258/nybp/nybp258b.17o.gz
    :param year_str: str
    :param day_str: str
    :param station_id: str
    :param repr_time_charactor: str: gps timestamp represent method a-x mapping to 0-24
    :param year_short_str: str: etc 2017 -> 17
    :return: str
    """
    link = "/".join((DEFAULT_URL, year_str, day_str, station_id,
                     station_id + day_str + repr_time_charactor + '.' + year_short_str + 'o.gz'))
    return link


def rinexlink(station_id, start_time, end_time, gap=0):
    """
    Get all of RINEX files' link by input station_id, start_time and end_time, it will return three kinds of formatting
    First condition: if interval is within one day, it will return {1: [list[datetime.obj]]},
    Second condition: if interval is two days, it will return {1: [list[datetime.obj], [list[datetime.obj]]]}
    the first list is start day all relate urls, the second list is end day all relate urls.
    Third condition: if interval is longer than 2 days, it will return {1: [list[datetime.obj], [list[datetime.obj]]]
    , 2: list[datetime.obj]} the key 1 structure is same as Second condition, the 2 key are store the days url base on
    days dir instead of file url. etc  /cors/rinex/2017/258/nybp/
    :param station_id: str
    :param start_time: datetime.obj
    :param end_time: datetime.obj
    :param gap: int
    :return: dict
    """
    day_term_list = timer_convertor.get_date_list(start_time, end_time, gap)
    datetime_plus_gap = timer_convertor.dateimeplus_gap(gap)
    start_time, _ = datetime_plus_gap(start_time)
    _, end_time = datetime_plus_gap(end_time)
    logging.info("Processing RINEX links from {} to {}".format(start_time, end_time))
    if len(day_term_list) == 2:
        if start_time.strftime("%d") == end_time.strftime("%d"):
            year_str, year_short_str, day_str = timer_convertor.datetimetostring(start_time)
            repr_time_charactors = timer_convertor.timetransfergpsinday(start_time, end_time)
            rinexlink = []
            for repr_time_charactor in repr_time_charactors:
                rinexlink.append(link_generator(year_str, day_str, station_id, repr_time_charactor, year_short_str))
            rinexlink.append(link_generator(year_str, day_str, station_id, '0', year_short_str))
            return {1: [rinexlink, ]}
        else:
            year_str_st, year_short_str_st, day_str_st = timer_convertor.datetimetostring(start_time)
            year_str_ed, year_short_str_ed, day_str_ed = timer_convertor.datetimetostring(end_time)
            repr_time_charactors_st = timer_convertor.timetransfergpsinday(start_time)
            repr_time_charactors_ed = timer_convertor.timetransfergpsinday(None, end_time)
            rinexlink_st = []
            for repr_time_charactor_st in repr_time_charactors_st:
                rinexlink_st.append(
                    link_generator(year_str_st, day_str_st, station_id, repr_time_charactor_st, year_short_str_st))
            rinexlink_st.append(link_generator(year_str_st, day_str_st, station_id, '0', year_short_str_st))
            rinexlink_ed = []
            for repr_time_charactor_ed in repr_time_charactors_ed:
                rinexlink_ed.append(
                    link_generator(year_str_ed, day_str_ed, station_id, repr_time_charactor_ed, year_short_str_ed))
            rinexlink_ed.append(link_generator(year_str_ed, day_str_ed, station_id, '0', year_short_str_ed))
            return {1: [rinexlink_st, rinexlink_ed]}
    else:
        year_str_st, year_short_str_st, day_str_st = timer_convertor.datetimetostring(start_time)
        year_str_ed, year_short_str_ed, day_str_ed = timer_convertor.datetimetostring(end_time)
        repr_time_charactors_st = timer_convertor.timetransfergpsinday(start_time)
        repr_time_charactors_ed = timer_convertor.timetransfergpsinday(None, end_time)
        other_day_list = day_term_list[1:len(day_term_list) - 1]
        rinexlink_st = []
        for repr_time_charactor_st in repr_time_charactors_st:
            rinexlink_st.append(
                link_generator(year_str_st, day_str_st, station_id, repr_time_charactor_st, year_short_str_st))
        rinexlink_st.append(link_generator(year_str_st, day_str_st, station_id, '0', year_short_str_st))
        rinexlink_ed = []
        for repr_time_charactor_ed in repr_time_charactors_ed:
            rinexlink_ed.append(
                link_generator(year_str_ed, day_str_ed, station_id, repr_time_charactor_ed, year_short_str_ed))
        rinexlink_ed.append(link_generator(year_str_ed, day_str_ed, station_id, '0', year_short_str_ed))
        rinexlink_other = []
        for other_day in other_day_list:
            year_str_ot, year_short_str_ot, day_str_ot = timer_convertor.datetimetostring(other_day)
            rinexlink_other.append("/".join((DEFAULT_URL, year_str_ot, day_str_ot, station_id + '/')))
        return {1: [rinexlink_st, rinexlink_ed], 2: rinexlink_other}
