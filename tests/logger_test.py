import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from logger.loggerfactory import LoggerFactory

def test_logger_conf():
    #logger = LoggerFactory('log_test.log').get_logger()
    logger_factory = LoggerFactory('log_test.log')
    logger = logger_factory.get_logger()

    print(logger.__dict__)
    handlers = logger.handlers
    assert len(handlers) == 2