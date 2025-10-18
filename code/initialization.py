import os
import logging
from datetime import datetime

from data import xml, DBClient, FileClient
from config import get_config

LOG_DIR = get_config()['LOG_DIR']
CLIENT = get_config()['CLIENT']
def init_database(debug_mode):
    if CLIENT.lower() == 'db':
        client = DBClient()
    else:
        client = FileClient()

    if not client.is_initialized():
        data = xml.load_data()
        logging.info("Loaded %s snippets successfully" % len(data))
        client.add_articles(data)


def init_logging(debug_mode, subprocess=False):
    """
    Initializes logging using the `logging` [module](https://docs.python.org/3/library/logging.html).
    Logs file at `LOG_FILE_PATH` as well as the terminal.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(filename)s:%(lineno)d] %(message)s")
    rootLogger = logging.getLogger()

    if debug_mode:
        # https://docs.python.org/3/library/logging.html#levels
        # 10 == DEBUG
        rootLogger.setLevel(10)
    
    

    if not subprocess:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)
    

    file_suffix = 'SUB' if subprocess else 'MAIN'
    time = "{:%Y-%m-%d-%H-%M-%S}".format(datetime.now())
    log_filename = "%s-%s.txt" % (time, file_suffix)

    fileHandler = logging.FileHandler(os.path.join(LOG_DIR, log_filename))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    



def init(debug_mode):
    """
    Performs any initialization that the application requires
    
    Right now, it just starts the logging framework.
    """
    init_logging(debug_mode)
    init_database(debug_mode)