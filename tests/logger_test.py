import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import logging
from logger.loggerfactory import LoggerFactory


def test_get_logger():
    logger = LoggerFactory().get_logger('test_logger', 'log_test.log')
    # Check that the returned logger instance is an instance of Logger
    assert isinstance(logger, logging.Logger)


def test_logger_conf():
    logger = LoggerFactory().get_logger('test_logger', 'log_test.log')

    # verify that handlers existence
    handlers = logger.handlers
    assert len(handlers) == 2
    # check formatting
    expected_format = "%(asctime)s - %(levelname)s - %(message)s"
    expected_date_format = "[%m/%d/%Y %H:%M:%S]"

    for handler in handlers:
        formatter = handler.formatter
        assert formatter._fmt == expected_format
        assert formatter.datefmt == expected_date_format

