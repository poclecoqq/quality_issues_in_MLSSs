import datetime
import pickle
from tqdm import tqdm
from pathlib import Path

from github_queries.user import get_n_results_github_user_search, search_users_github, fetch_user_email
from utils import save_user_ids, save_emails


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


def fetch_users_email(users_id):
    """
    Fetches the email associated with a user profile,
    given a list of users id.
    Input:
        users_id: a list of users id
    Output:
        emails: a list of email addresses

    """
    print(f'---------------- Fetching emails from user ids ----------------')
    emails = []
    try:
        for user_id in tqdm(users_id):
            email = fetch_user_email(user_id)
            if not email is None:
                emails.append(email)
        return emails
    except Exception as e:
        save_emails(emails, suffix=f"user_search-partial-results")
        raise Exception("Could not fetch all emails.") from e


def main(tags):
    for tag in tags:
        tag_suffix = "-".join(tag.split(" ")).lower()
        # Search for users matching some keyword
        users_id = fetch_all_users_ids(tag)
        save_user_ids(users_id, suffix=f"user_search-{tag_suffix}")
        emails = fetch_users_email(users_id)
        save_emails(emails, suffix=f"user_search-{tag_suffix}")
        print(f"\n** Fetched {len(emails)} emails! **\n")


if __name__ == "__main__":
    # tags = ["Machine Learning Engineer", "Data Scientist"]
    tags = ['Data Scientist']
    main(tags)
