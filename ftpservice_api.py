import ftplib
import os
import re
import logging

from dateutil import parser


class ftp_file:

    def __init__(self, url='www.ngs.noaa.gov', user=None, password=None, acct=None, timeout=None):
        """
        Init ftp connection, and get ftp object, we can set up url, login user/password, also retry times
        and timeout.
        :param url: str
        :param user: str
        :param password: str
        :param acct: int
        :param timeout: int
        """
        self.url = url
        try:
            self.ftp = ftplib.FTP(self.url, acct=acct, timeout=timeout)
        except Exception as e:
            logging.error("Connection failed due to : {}".format(e))
        self.ftp.login(user, password)
        self.ftp.sendcmd('PASV')

    # def is_same_size(self, file_orig, file_copy_local):
    #
    #     try:
    #         remote_file_size = self.ftp.size(file_orig)
    #     except Exception as err:
    #         # self.debug_print("is_same_size() ：%s" % err)
    #         remote_file_size = -1
    #
    #     try:
    #         local_file_size = os.path.getsize(file_copy_local)
    #     except Exception as err:
    #             # self.debug_print("is_same_size() ：%s" % err)
    #         local_file_size = -1
    #
    #     print('local_file_size:%d  , remote_file_size:%d' % (local_file_size, remote_file_size))
    #     if remote_file_size == local_file_size:
    #         return 1
    #     else:
    #         return 0

    def download_file(self, file_orig, file_copy_local):
        logging.info("download_file()---> local_path = {} ,remote_path = {}".format(file_copy_local, file_orig))
        try:
            logging.info('>>>>>>>>>>>>download file {} ... ...'.format(file_copy_local))
            buf_size = 1024
            file_handler = open(file_copy_local, 'wb')
            self.ftp.retrbinary('RETR {}'.format(file_orig), file_handler.write, buf_size)
            file_handler.close()
        except Exception as err:
            logging.warning('download error：{}'.format(err))
            return


    def download_file_bk(self, file_orig, file_copy_local):
        """
        Download file from FTP server, please provide the ftp file url, also provide local file store path
        and file name, if success download file it will return True,
        :param file_orig: str
        :param file_copy_local: str
        :return: bool
        """
        print("Processing link : {}".format(file_orig))
        print("local_file is: {}".format(file_copy_local))
        with open(file_copy_local, 'w') as fp:
            try:
                res = self.ftp.retrlines('RETR ' + file_orig, fp.write)
                print("res : {}".format(res))
                if not res.startswith('226 Transfer complete'):
                    print('Download failed')
                    if os.path.isfile(file_copy_local):
                        os.remove(file_copy_local)
                return True
            except Exception as e:
                print("File Not Found : {}".format(e))
                return False

    def getfiles(self, path, filter=""):
        """
        Get file list with regex filter from ftp server, path is remote ftp server dir, if will return the full file
        list from remote ftp server, and then filter by regex will filter out the file we want.
        :param path: str
        :param filter: str
        :return: list[file name]
        """
        try:
            self.ftp.cwd(path)
            filelist = self.ftp.nlst()
            filter_complier = re.compile(filter)
        except Exception as e:
            raise Exception("{} Path Can't be found".format(path))
        return [file_name for file_name in filelist if filter_complier.match(file_name)]

    def getfilesdetail(self, path):
        """
        Get full list of files from specify dir, and also with timestamp for each file name
        :param path: str
        :return: list[]
        """
        dir_files = []
        file_name_time_list = []
        try:
            self.ftp.cwd(path)
            self.ftp.dir(dir_files.append)
        except Exception as e:
            raise Exception("{} Path Can't be found".format(path))
        for file_inf in dir_files:
            tokens = file_inf.split(maxsplit=9)
            file_name = tokens[8]
            time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
            file_time = parser.parse(time_str)
            file_name_time_list.append((file_name, file_time))
        return (file_name_time_list)

    def __del__(self):
        self.ftp.quit()
