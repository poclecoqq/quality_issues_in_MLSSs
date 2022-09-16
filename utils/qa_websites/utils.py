import logging
from pathlib import Path
import os
import pickle
import pandas as pd
from datetime import datetime

PATH = Path(__file__).parent.resolve()
DATA_PATH = Path(PATH, 'data')
os.makedirs(DATA_PATH, exist_ok=True)


def init_logger():
    """
    Initializes the logger of the script.
    Logs to file and to terminal.
    Output:
        logger
    """
    logger = logging.getLogger('scope.name')

    t = datetime.timestamp(datetime.now())
    f_path = Path(DATA_PATH, f'logfile-{t}.txt')
    file_log_handler = logging.FileHandler(f_path)
    logger.addHandler(file_log_handler)

    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)
    # Log everything it receives
    logger.setLevel('DEBUG')

    return logger


def get_key(website, user_category="", period="", tag=""):
    return ' '.join([website, user_category, period, tag])


def save_file(file_name, obj):
    """
    Saves any object to data dir using pickle.
    Input:
        file_name: The name of the file storing the object
        obj: The object to save
    """
    f_path = Path(DATA_PATH, file_name)
    with open(f_path, "wb") as f:
        pickle.dump(obj, f)


def load_file(file_name):
    """
    Loads an object using pickle.
    Input:
        file_name: The name of the file storing the pickle object
    Output:
        obj: The object
    """
    f_path = Path(DATA_PATH, file_name)
    with open(f_path, "rb") as f:
        obj = pickle.load(f)
    return obj


def save_to_csv(file_name, d):
    """
    Save to csv the results of the script that
    are saved in a dict. It expects the dict's keys
    to follow 'get_key' function's nomenclature.
    """
    websites, user_categories, periods, tags, web_handles_f = [], [], [], [], []
    for key, web_handles in d.items():
        website, user_category, period, tag = key.split(' ')
        for web_handle in web_handles:
            websites.append(website)
            user_categories.append(user_category)
            periods.append(period)
            tags.append(tag)
            web_handles_f.append(web_handle)
    df = pd.DataFrame({'website': websites, 'user_category': user_categories,
                      'period': periods, 'tag': tags, 'web_handle': web_handles_f})
    f_path = Path(DATA_PATH, file_name)
    df.to_csv(f_path, index=False)
