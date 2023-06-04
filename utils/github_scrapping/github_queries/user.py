import requests
from .token import token_provider


def get_n_results_github_user_search(tag, start_date, end_date):
    """
    Returns the number of results for a given 
    user search
    Input:
        tag: The keyword used to perform the search
        start_date: 
        end_date:
    Output:
        number of users
    """
    token = token_provider.get_token('search')
    url = f'https://api.github.com/search/users?q="{tag}" type:user created:{start_date}..{end_date}'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=headers)
    res = res.json()
    return res['total_count']


def search_users_github(tag, start_date, end_date, page_n):
    """
    Performs user search.
    Input:
        tag: The keyword used to perform the search
        start_date: 
        end_date:
    Output:
        user_ids: a list of user ids
    """
    token = token_provider.get_token('search')
    url = f'https://api.github.com/search/users?q="{tag}" type:user created:{start_date}..{end_date}&page={page_n}'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=headers)
    res = res.json()

    # Extract user ids
    user_ids = []
    for user_profile in res['items']:
        user_ids.append(user_profile['login'])
    return user_ids


def fetch_user_email(user_id):
    token = token_provider.get_token('core')
    url = f'https://api.github.com/users/{user_id}'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=headers)
    res = res.json()
    return res.get('email')
