import pickle
import json
from pathlib import Path
import time

ts = str(int(time.time()))
crnt_dir = Path(__file__).parent.resolve()
data_dir = Path(crnt_dir, "data", ts)
data_dir.mkdir(parents=True, exist_ok=True)


def _save_arr_to_text(f_path, arr):
    with open(f_path, 'w') as f:
        json.dump(arr, f)


def _save_pickle(f_path, obj):
    with open(f_path, 'wb') as f:
        pickle.dump(obj, f)


def _load_pickle(f_path):
    with open(f_path, 'rb') as f:
        obj = pickle.load(f)
    return obj


def save_emails(emails, suffix=""):
    email_txt_path = Path(data_dir, f"emails-{suffix}.txt")
    _save_arr_to_text(email_txt_path, emails)
    email_bin_path = Path(data_dir, f"emails-{suffix}.bin")
    _save_pickle(email_bin_path, emails)


def save_user_ids(user_ids, suffix=""):
    users_id_bin_path = Path(data_dir, f"users_id-{suffix}.bin")
    _save_pickle(users_id_bin_path, user_ids)


def load_user_ids(timestamp, suffix=""):
    dir = Path(crnt_dir, "data", timestamp)
    users_id_bin_path = Path(dir, f"users_id-{suffix}.bin")
    return _load_pickle(users_id_bin_path)
