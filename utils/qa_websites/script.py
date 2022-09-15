from collections import defaultdict
from copyreg import pickle
from pathlib import Path
import os
from typing import List
import requests
import json
import pickle

PATH = Path(__file__).parent.resolve()
DATA_PATH = Path(PATH, 'data')
os.makedirs(DATA_PATH, exist_ok=True)


def get_key(tag, user_category, period):
    return f'{tag}-{user_category}-{period}'


def get_top_users_id(website: List, tags: List, n_results=100, verbose=False) -> List:
    """
    Gets top users' id for a set of tags for a given websites.
    Top users a fetched from two categories: "all_time" and "month"
    Input:
        website_url:
        tags:
        n_results: number of users returned
    Output:
        users: a list of user ids
    """
    ans = {}
    for tag in tags:
        if verbose:
            print(f'Fetching top users on "{website}" for the tag "{tag}."')
        params = {'pagesize': n_results, 'site': website}
        for user_category in ['top-askers', 'top-answerers']:
            for period in ['all_time', 'month']:
                url = f'https://api.stackexchange.com/2.3/tags/{tag}/{user_category}/{period}'
                res = requests.get(url, params=params)
                parsed_response = json.loads(res.text)
                # Print if verbose
                if verbose:
                    n_users = len(parsed_response['items'])
                    print(
                        f'\t{user_category}-{period} number of users: {n_users}')
                # Extract the users id from the results
                user_ids = []
                for user in parsed_response['items']:
                    user_ids.append(user['user']['user_id'])
                k = get_key(tag, user_category, period)
                ans[k] = user_ids
    return ans


if __name__ == "__main__":
    website = 'stackoverflow'  # 'datascience'
    tags = ['machine-learning']
    users_id = get_top_users_id(website, tags, verbose=True)
    with open("state.bin", "wb") as f:
        pickle.dump(users_id, f)
    with open(Path("state.bin"), "rb") as f:  # "rb" because we want to read in binary mode
        state = pickle.load(f)
    print(state)
