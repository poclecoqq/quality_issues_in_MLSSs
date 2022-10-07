import datetime
import pickle
from tqdm import tqdm

from github_queries.user import get_n_results_github_user_search, search_users_github


def fetch_all_users_ids(tag):
    """
    Fetches all users matching some keyword (i.e. tag).
    Input:
        tag: The keyword used to perform the search
    Output:
        user_ids
    """
    def fetch_all_users_ids_rec(tag, start_date, end_date):
        """
        The recursive function for fetch_all_users_ids function.
        Divides the time period by 2 if there is too much results.
        Output:
            user_ids
        """
        n_results = get_n_results_github_user_search(
            tag, start_date.isoformat(), end_date.isoformat())
        GITHUB_MAX_RESULTS = 1000
        if n_results >= GITHUB_MAX_RESULTS:
            mid_date = start_date + (end_date-start_date)/2
            user_ids_l = fetch_all_users_ids_rec(tag, start_date, mid_date)
            user_ids_r = fetch_all_users_ids_rec(tag, mid_date, end_date)
            return user_ids_l + user_ids_r
        else:
            user_ids = []
            page_n = 1
            while len(user_ids) < n_results:
                user_ids += search_users_github(tag, start_date.isoformat(),
                                                end_date.isoformat(), page_n)
                page_n += 1

            nonlocal progress
            progress += len(user_ids)
            print(f'{progress}/{tot_n_results}')
            return user_ids

    # Github cration date (-1 day)
    start_date = datetime.date(2008, 10, 18)
    end_date = datetime.datetime.now().date()
    progress = 0
    tot_n_results = get_n_results_github_user_search(
        tag, start_date.isoformat(), end_date.isoformat())

    print(
        f'---------------- User search with keyword "{tag}" ----------------')
    return fetch_all_users_ids_rec(tag, start_date, end_date)


if __name__ == "__main__":
    a = fetch_all_users_ids("Machine Learning Engineer")
    print(a)
    with open("tmp.bin", 'wb') as f:
        pickle.dump(a, f)
