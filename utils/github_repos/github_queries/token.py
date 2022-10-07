from collections import defaultdict
import yaml
from pathlib import Path
import requests
import pause


class TokenProvider():
    QUERY_TYPES = ['core', 'search']

    def __init__(self):
        self.tokens = self._fetch_tokens()
        self.token_idx = defaultdict(int)

    def _fetch_tokens(self):
        crnt_dir = Path(__file__).parent.resolve()
        config_file_path = Path(crnt_dir, "config.yaml")
        with open(config_file_path, "r") as f:
            config = yaml.safe_load(f)
            return config['tokens']

    def get_token(self, query_type):
        """
        Returns a token to send a request to GitHub.
        More precisly, it returns the least recently used token. If
        the token has reached its rate limit for the desired query type
        (i.e. search or core), then it will pause the program until
        the token's rate is reset (i.e. the token can be used to send requests)
        Input:
            query_type: the type of the query that will use that token (i.e. search or core)
        """
        assert query_type in TokenProvider.QUERY_TYPES
        token = self.tokens[self.token_idx[query_type]]
        # Measure how many request are left with that token
        url = f'https://api.github.com/rate_limit'
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}"
        }
        res = requests.get(url, headers=headers)
        res = res.json()
        # If the token has reached its limit of request for that type of request, wait until the counter is reset
        if res['resources'][query_type]['remaining'] == 0:
            pause.until(res['resources'][query_type]['reset'])

        # Increment token idx
        self.token_idx[query_type] = (
            self.token_idx[query_type] + 1) % len(self.tokens)
        return token


token_provider = TokenProvider()
