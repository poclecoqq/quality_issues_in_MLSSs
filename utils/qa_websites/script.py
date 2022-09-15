from pathlib import Path
import os
from typing import List
import requests
import json

PATH = Path(__file__).parent.resolve()
DATA_PATH = Path(PATH, 'data')
os.makedirs(DATA_PATH, exist_ok=True)


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
    for tag in tags:
        if verbose:
            print(f'Fetching top users on "{website}" for the tag "{tag}."')
        params = {'pagesize': n_results, 'site': website}
        responses = []
        for period in ['all_time', 'month']:
            url = f'https://api.stackexchange.com/2.3/tags/{tag}/top-askers/{period}'
            res = requests.get(url, params=params)
            responses.append(res)
        # Extract the users id from the results
        user_ids = []
        for response in responses:
            parsed_response = json.loads(response.text)
            if verbose:
                n_users = len(parsed_response['items'])
                print(f'Number of users: {n_users}')
            for user in parsed_response['items']:
                user_ids.append(user['user']['user_id'])
    return user_ids


if __name__ == "__main__":
    website = 'stackoverflow'  # 'datascience'
    tags = ['machine-learning']
    a = get_top_users_id(website, tags, verbose=True)
    print(a)
