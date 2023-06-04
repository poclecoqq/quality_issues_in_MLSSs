# utils

This folder holds all the Python scripts we used during the study. There are 3 subfolders: `github_repos`, `plots`, and `qa_websites`. Below, we briefly describe the folders. 

## `github_repos`
This folder contains the code we used to fetch email addresses from the GitHub API, as described in our paper. The script can be launched from `scrape_users.py`. The keywords used to fetch user profiles are in the aforementioned file. Thus, if desired, the script could be used to fetch user using different keywords. Before running the script, the user must provide its [GitHub API access tokens](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api?apiVersion=2022-11-28#about-tokens) in a file named `config.py` in the `github_queries` sobfolder. Here is the template for the file. The email addresses are printed in a text file in the output folder named `data` (created automatically when running the script).
``` yaml
tokens:
  - "TOKEN"
```

## `plots`
This folders contains the code used to generate the plots in our paper.


## `qa_websites`
This folder contains the code we used to fetch user profiles from Q&A platforms  as described in our paper. It fetches user profiles from Data Science Stack Exchange and Stack Overflow using tags (i.e. keywords) that can be changed inside the code. To fetch user profiles, launch the `script.py` file


