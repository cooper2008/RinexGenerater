import os
import unittest
from datetime import datetime
import logging

import RINEXlinkgenerator
import ftpservice_api
import timer_convertor


rinex_result_case1 = ['/cors/rinex/2020/039/1nsu/1nsu039p.20o.gz', '/cors/rinex/2020/039/1nsu/1nsu039q.20o.gz',
                      '/cors/rinex/2020/039/1nsu/1nsu039r.20o.gz', '/cors/rinex/2020/039/1nsu/1nsu0390.20o.gz']


class TestftpApi(unittest.TestCase):

    def setUp(self):
        self.ftp_obj = ftpservice_api.ftp_file()
        self.download_link = '/cors/rinex/2020/056/1nsu/1nsu0560.20S'
        self.localfile = './test_download_folder/1nsu0560.20S'
        self.remote_dir = '/cors/rinex/2020/054/1nsu/'

    def testdownloadFile(self):
        self.ftp_obj.download_file(self.download_link, self.localfile)
        if os.path.exists(self.localfile):
            fsize = os.path.getsize(self.localfile)
            os.remove(self.localfile)
        self.assertEqual(fsize, 42518)

    def testListFile(self):
        filelist = self.ftp_obj.getfiles(self.remote_dir, ".*\.20o\.gz$")
        self.assertEqual(filelist, ['1nsu0540.20o.gz'])


class TestTimeconvertor(unittest.TestCase):

    def setUp(self):
        self.testDaytime_1 = datetime(2020, 2, 8, 15, 23, 40)
        self.testDaytime_2 = datetime(2020, 2, 8, 20, 23, 40)
        self.testDaytime_3 = datetime(2020, 2, 5, 17, 23, 40)
        self.dateString = '2020-02-25T09:11:22Z'

    def testtimeTransfertogpsFormat(self):
        timer_convert_test1 = timer_convertor.timetransfergpsinday(self.testDaytime_1)
        timer_convert_test2 = timer_convertor.timetransfergpsinday(None, self.testDaytime_2)
        timer_convert_test3 = timer_convertor.timetransfergpsinday(self.testDaytime_1, self.testDaytime_2)
        self.assertEqual(timer_convert_test1, ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x'])
        self.assertEqual(timer_convert_test2,
                         ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                          't', 'u'])
        self.assertEqual(timer_convert_test3, ['p', 'q', 'r', 's', 't', 'u'])

    def testDayTimetoString(self):
        dateTimetoString_1 = timer_convertor.datetimetostring(self.testDaytime_1)
        self.assertEqual(dateTimetoString_1, ('2020', '20', '039'))

    def testStringtoDatetime(self):
        str_datetime_convertor = timer_convertor.string2datetime('%Y-%m-%dT%H:%M:%SZ')
        transfer_datetime = str_datetime_convertor(self.dateString)
        self.assertEqual(transfer_datetime, datetime(2020, 2, 25, 9, 11, 22))

    def testGetDaylist(self):
        getdaylist = timer_convertor.get_date_list(self.testDaytime_3, self.testDaytime_1)
        self.assertEqual(getdaylist, [datetime(2020, 2, 5, 17, 23, 40), datetime(2020, 2, 6, 17, 23, 40),
                                      datetime(2020, 2, 7, 17, 23, 40), datetime(2020, 2, 8, 15, 23, 40)])


class TestRinexlinkGenerator(unittest.TestCase):

    def setUp(self):
        self.station_id = '1nsu'
        self.start_time = datetime(2020, 2, 8, 15, 23, 40)
        self.end_time_1 = datetime(2020, 2, 8, 17, 23, 40)
        self.end_time_2 = datetime(2020, 2, 9, 14, 23, 40)
        self.end_time_3 = datetime(2020, 2, 9, 15, 21, 15)

    def testLinkgenerator(self):
        rinexlinks_test1 = RINEXlinkgenerator.rinexlink(self.station_id, self.start_time, self.end_time_1)
        # rinexlinks_test2 = RINEXlinkgenerator.rinexlink(self.station_id, self.start_time, self.end_time_2)
        # rinexlinks_test3 = RINEXlinkgenerator.rinexlink(self.station_id, self.start_time, self.end_time_3)
        print(rinexlinks_test1[1][0])
        self.assertEqual(rinexlinks_test1[1][0], rinex_result_case1)


if __name__ == '__main__':
    unittest.main()
