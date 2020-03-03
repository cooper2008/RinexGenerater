__author__ = 'Cooper Guo'
import getopt
import logging
import os
import re
import subprocess
import sys
from datetime import datetime

from RINEXlinkgenerator import rinexlink
from exception_handler import st_et_input_exception_handler
from exception_handler import time_parms_handler
from ftpservice_api import ftp_file
from local_files_api import decompress_files
from local_files_api import list_local_dir
from local_files_api import removefiles
from timer_convertor import string2datetime

GNSS_URL = "www.ngs.noaa.gov"
LOCAL_PATH = "./mergefiles_folder"
CURRENT_PATH = os.path.abspath('.')
os.environ['PATH'] += ":" + CURRENT_PATH

logging.basicConfig(
    level=logging.DEBUG,
    format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename="/tmp/RINEXgenerator.log",
    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def file_list_filter(file_list, pattern):
    """
    Use regex in pattern to filter out the list
    :param file_list: list
    :param pattern: str
    :return: list
    """
    achieve_file_filter = re.compile(pattern)
    return [file_name for file_name in file_list if achieve_file_filter.match(file_name)]


def ftp_download_files(list_dict):
    """
    download the ftp files by dict from RINEXlinkgenerator.py, the detail condition please check in
    RINEXlinkgenerator.rinexlink, there are three conditions.
    1. interval one day, it will only have {1: [list[datetime.obj]]}, it will download all of the files, unless it
    only have achieve file, then it will download achieve file as well
    2. interval two days, it will have {1: [list[datetime.obj], [list[datetime.obj]]]}, and it will download all
    of two list url files
    3. interval longer than 2 days, it will have dict like: {1: [list[datetime.obj], [list[datetime.obj]]]
    , 2: list[datetime.obj]}, download all files as step2,  then process key2 in dict, list all of files from ftp
    server by their dir link, and use filter to findout all of relate gz files, then download all days files.
    :param list_dict: dict
    :return: void
    """
    try:
        Process_for_stage1 = list_dict[1]
    except Exception as e:
        raise Exception("No file list can be found")
    logging.info("Dowloading Files from FTP server")
    ftp_obj = ftp_file(GNSS_URL)
    if len(Process_for_stage1) == 1:
        logging.info("One Day Interval for Files")
        remove_list = []
        for i, file_url in enumerate(Process_for_stage1[0]):
            if i != len(Process_for_stage1[0]) - 1:
                local_file = "/".join((LOCAL_PATH, os.path.basename(file_url)))
                remove_list.append(local_file)
                response = ftp_obj.download_file(file_url, local_file)
                if not response:
                    logging.info("Processing achivev file : {}".format(Process_for_stage1[0][-1]))
                    local_file = "/".join((LOCAL_PATH, os.path.basename(Process_for_stage1[0][-1])))
                    ftp_obj.download_file(Process_for_stage1[0][-1], local_file)
                    logging.info("remove files {}".format(remove_list))
                    removefiles(remove_list)
                    break

    else:
        logging.info("Two days Interval files to be processed")
        remove_list_st = []
        remove_list_ed = []
        for i, file_url in enumerate(Process_for_stage1[0]):
            if i != len(Process_for_stage1[0]) - 1:
                local_file = "/".join((LOCAL_PATH, os.path.basename(file_url)))
                remove_list_st.append(local_file)
                response = ftp_obj.download_file(file_url, local_file)
                if not response:
                    logging.info("Processing achieve file : {}".format(Process_for_stage1[0][-1]))
                    local_file = "/".join((LOCAL_PATH, os.path.basename(Process_for_stage1[0][-1])))
                    ftp_obj.download_file(Process_for_stage1[0][-1], local_file)
                    logging.info("remove files {}".format(remove_list_st))
                    removefiles(remove_list_st)
                    break
        for i, file_url in enumerate(Process_for_stage1[1]):
            if i != len(Process_for_stage1[1]) - 1:
                local_file = "/".join((LOCAL_PATH, os.path.basename(file_url)))
                remove_list_ed.append(local_file)
                response = ftp_obj.download_file(file_url, local_file)
                logging.info("response : {}".format(response))
                if not response:
                    logging.info("Processing achieve file : {}".format(Process_for_stage1[1][-1]))
                    local_file = "/".join((LOCAL_PATH, os.path.basename(Process_for_stage1[1][-1])))
                    ftp_obj.download_file(Process_for_stage1[1][-1], local_file)
                    removefiles(remove_list_ed)
                    break
    try:
        Process_for_stage2 = list_dict[2]
    except Exception as e:
        Process_for_stage2 = None
    if Process_for_stage2:
        for url_path_dir in Process_for_stage2:
            filelist = ftp_obj.getfiles(url_path_dir, "\w{4}\d{3}\w{1}\.\d{2}.{1}\.gz$")
            if file_list_filter(filelist, "\w{4}\d{3}0\.\d{2}.{1}\.gz$"):
                url_path = "/".join((url_path_dir, file_list_filter(filelist, "\w{4}\d{3}0\.\d{2}.{1}\.gz$")[0]))
                local_file = "/".join((LOCAL_PATH, file_list_filter(filelist, "\w{4}\d{3}0\.\d{2}.{1}\.gz$")[0]))
                ftp_obj.download_file(url_path, local_file)
            else:
                for file_name in filelist:
                    url_path = "/".join((url_path_dir, file_name))
                    local_file = "/".join((LOCAL_PATH, file_name))
                    ftp_obj.download_file(url_path, local_file)


if __name__ == "__main__":
    # Start generate files process
    logging.info("Start Process Generate the data")
    timestring_convertor = string2datetime('%Y-%m-%dT%H:%M:%SZ')
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:r:s:e:", ["station=", "ratio=", "start=", "end="])
    except getopt.GetoptError as err:
        # print help information and exit:
        logging.error(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    if len(opts) != 4:
        raise Exception("Please ensure you already input 4 args including station_id, gap, start_time, end_time")
    else:
        for o, a in opts:
            st_parms_handler = time_parms_handler('start_time')
            ed_parms_handler = time_parms_handler('end_time')
            if o in ("-n", "--stationId"):
                station_id = a
            elif o in ("-r", "--ratio"):
                ratio = a
            elif o in ("-s", "--start"):
                st_parms_handler(a)
                start_time = timestring_convertor(a)
            elif o in ("-e", "--end"):
                ed_parms_handler = a
                end_time = timestring_convertor(a)
            else:
                assert False, "unhandled option"

    logging.info("Input Parms : ", station_id, ratio, start_time, end_time)
    logging.info("Current Running Path : {}".format(os.environ['PATH']))
    ratio = int(ratio)
    st_et_input_exception_handler(start_time, end_time)
    rinex_links = rinexlink(station_id, start_time, end_time, ratio)
    logging.info(rinex_links)
    ftp_download_files(rinex_links)
    # Processing local files from gz -> unzip -> merge file
    donwnload_file_list = list_local_dir(LOCAL_PATH, ".*\.gz")
    logging.info("Downloaded all of gz files in {} including {}".format(LOCAL_PATH, donwnload_file_list))
    decompress_files(donwnload_file_list)
    removefiles(donwnload_file_list)
    o_file_list = list_local_dir(LOCAL_PATH, ".*o$")
    logging.info("All RINEX files : {}".format(o_file_list))
    cmd = "teqc {} > ./mergefiles_folder/RINEXdataset{}.obs".format(" ".join(o_file_list),
                                                                    datetime.utcnow().strftime("%Y-%M-%dT%H:%M:%S"))
    logging.info("Executing CMD : {}".format(cmd))
    out_bytes = subprocess.check_output(cmd, shell=True)
    removefiles(o_file_list)
    logging.info("Process completed!, Please check in mergefiles_folder")
