"""
class to handle log file inputs
"""

import logging
import logging.config
import os

log_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/niv/logs/niv.log'


class Nivlogger:
    """
    class for generating log entries
    """
    logging.basicConfig(filename=log_file_path,
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')

    @staticmethod
    def log_error(log_message):
        """
        function to clear log file and input error messages
        """
        with open(log_file_path, 'w'):
            pass
        logging.error(log_message, exc_info=True)

    @staticmethod
    def log(log_message):
        """
        function to add input to log file
        """
        logging.info("%s \n", log_message)
