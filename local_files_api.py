import gzip
import os
import re
from os import listdir
from os.path import  isfile, join
import logging

def decompress_files(gz_list):
    """
    decompress all files under path
    :param gz_list: list
    :return:
    """
    for gz_file in gz_list:
        try:
            input = gzip.GzipFile(gz_file, 'rb')
            s = input.read()
            input.close()
            output = open(gz_file.replace(".gz",""), 'wb')
            output.write(s)
            output.close()
        except Exception as e:
            logging.error("Open File with Error : {}".format(e))


def list_local_dir(local_dir, filter=""):
    """
    List out all of the files under local path
    :param local_dir:
    :return:
    """
    filter_complier = re.compile(filter)
    return ["/".join((local_dir,file)) for file in listdir(local_dir) if isfile(join(local_dir, file))
            and filter_complier.match(file)]

def removefiles(file_path_list):
    """
    Remove list out files from local path
    :param file_path_list: list
    :return: void
    """
    for file_path in file_path_list:
        try:
            os.remove(file_path)
        except FileNotFoundError as e:
            logging.error("File not found")

