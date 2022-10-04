import logging
from pathlib import Path
import os
import pickle
import pandas as pd
from datetime import datetime
import numpy as np

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
    # Create log dir if it does not exists
    log_dir = Path(DATA_PATH, 'logfiles')
    log_dir.mkdir(parents=True, exist_ok=True)
    # Create log file
    t = datetime.timestamp(datetime.now())
    f_path = Path(log_dir, f'logfile-{t}.txt')
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


def result_dic_to_df(d):
    """
    Transforms the results stored in the result dictionnary
    into a dataframe. It expects the dict's keys
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
    return df


def save_results(d):
    """
    Save to csv the results of the script that
    are saved in a dict. It expects the dict's keys
    to follow 'get_key' function's nomenclature. If 
    merge_old_results is set to True, it will try
    to read the results from a previous run, looking for a 
    file named file_name.
    Input:
        file_name: The file name used to look for previous results and to save the final results.
        d: The dictionnary with the results of the run
        merge_old_results: Whether to merge current results to previous results
    """
    df = result_dic_to_df(d)
    f_path = Path(DATA_PATH, 'final.csv')

    new_web_handles = set(df['web_handle'].unique())
    # If we want to use previous results and the file exists
    if f_path.exists():
        # Read previous results
        old_df = pd.read_csv(f_path, keep_default_na=False)
        # Update the set of new web handles by removing old ones
        old_web_handles = set(old_df['web_handle'].unique())
        new_web_handles = new_web_handles - old_web_handles
        # Merge dataframe
        df = pd.concat([old_df, df])
        df = df.drop_duplicates()
    df.to_csv(f_path, index=False)

    f_path = Path(DATA_PATH, 'new_emails.txt')
    with open(f_path, 'w') as f:
        for new_web_handle in new_web_handles:
            f.write(f'{new_web_handle}\n')
    return df
