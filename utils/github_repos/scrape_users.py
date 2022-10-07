import requests
from utils import TokenProvider
import datetime

token_provider = TokenProvider()


def get_n_results_github_user_search(tag, start_date, end_date):
    token = token_provider.get_token('search')
    url = f'https://api.github.com/search/users?q="{tag}" type:user created:{start_date}..{end_date}'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=headers)
    res = res.json()
    return res['total_count']


def search_users_github(tag, start_date, end_date):
    url = f'https://api.github.com/search/users?q="{tag}" type:user &page=100'


if __name__ == "__main__":
    now = datetime.datetime.now().isoformat()
    # Actually, GitHub was created the next day..
    GITHUB_CREATION_DATE = datetime.date(2008, 10, 18).isoformat()
    a = get_n_results_github_user_search(
        "Machine Learning Engineer", GITHUB_CREATION_DATE, now)
    print(a)
