import logging
from fs import FS

class AppLogger:
    """
    This is extremely important and I'm not a fan of printing to stdout/stderr
    However, logging is necessary, and while print is slow, logging to files is.. also slow
    - still, we can separate it to a class like this and maybe log to files only locally
    otherwise logging to graylog
    Or I could add graylog to docker-compose and just change the hostname depending on the environment..
    All in all, centralized logging is a must, and this is a good start as any.
    """
    def __init__(self, logger_name: str = "docusense"):
        self.fs = FS()
        self.logger = logging.getLogger(logger_name)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
        try:
            file_handler = logging.FileHandler(self.fs.log_file, mode="a")
            file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.info(f"File logging activated: {self.fs.log_file}")
        except Exception as e:
            self.logger.error(f"Failed to set up file logging at {self.fs.log_file}: {e}")
            exit(1)

    def get_logger(self):
        return self.logger
