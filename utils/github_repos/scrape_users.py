import datetime
from github_queries.user import get_n_results_github_user_search, search_users_github

if __name__ == "__main__":
    now = datetime.datetime.now().isoformat()
    # Actually, GitHub was created the next day..
    GITHUB_CREATION_DATE = datetime.date(2008, 10, 18).isoformat()
    a = get_n_results_github_user_search(
        "Machine Learning Engineer", GITHUB_CREATION_DATE, now)
    print(a)
    a = search_users_github(
        "Machine Learning Engineer", GITHUB_CREATION_DATE, now, 1)
    print(a)
    print(len(a))
