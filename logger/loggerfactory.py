import logging

class LoggerFactory:
    def __init__(self, log_file_path):
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="[%m/%d/%Y %H:%M:%S]",
            level=logging.INFO,
            handlers=[
                logging.FileHandler(log_file_path),  # File output
                logging.StreamHandler()  # Console output
            ]
        )
        self.logger = logging.getLogger(log_file_path)


    def get_logger(self):
        return self.logger