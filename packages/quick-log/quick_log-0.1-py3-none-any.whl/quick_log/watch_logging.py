# -*- coding=utf-8 -*-
import os
import logging
from logging import FileHandler
from datetime import datetime

LEVEL = {
    "debug": logging.DEBUG, #10
    "info": logging.INFO,   #20
    "warn": logging.WARN,   #30
    "error": logging.ERROR, #40
    "fatal": logging.FATAL, #50
}

def create_file_logger(app_name, log_level="debug", format='%(lineno)04s: %(asctime)s %(name)-12s: %(levelname)s %(message)s', file_base="./"):
    logger = logging.getLogger(f"{app_name}_log")
    formatter = logging.Formatter(format)
    handler = FileHandler(os.path.join(file_base,"%s_%s.log" % (app_name, datetime.now().strftime("%Y%m%d_%H:%M:%S"))))
    logger.setLevel(LEVEL[log_level])
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

