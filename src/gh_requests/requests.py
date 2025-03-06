
from github import Github
import os
from gh_requests.exclude_loc import is_excluded_file

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def lines_of_code_by_repo(owner: str, repo_name: str) -> dict[str, int]: 
    """
    Returns a dict containing the repo and the total lines of code in the repo 
    """

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{owner}/{repo_name}")

    total_lines = 0

    def count_lines_in_dir(directory_path=""): 
        nonlocal total_lines
        contents = repo.get_contents(directory_path)

        # If contents is a list, it is a directory
        for content_file in contents: 
            if content_file.type == "dir": 
                # Recursively call the function if it's a subdirectory
                count_lines_in_dir(content_file.path)
            else: 
                # If it's a file, count its lines
                if not is_excluded_file(content_file):  
                    file_content = repo.get_contents(content_file.path)
                    # Decode the file content and count lines
                    file_lines = len(file_content.decoded_content.decode('utf-8').splitlines())
                    total_lines += file_lines
                    print(f"File: {content_file.path}, Lines: {file_lines}")



    count_lines_in_dir()
    return { repo_name: total_lines }



def lines_of_code_by_user(owner: str, repo_name: str) -> dict[str, int]: 
    """
    Returns a dict containng usernames and the total lines of 
    code they have contributed to the repo 

    """
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{owner}/{repo_name}")

    contributers = repo.get_contributors()
    
    user_line_counts = {}

    for contributer in contributers: 
        commits = repo.get_commits(author=contributer)
        total_lines = 0

        for commit in commits: 
            for file in commit.files: 
                if is_excluded_file(file): 
                    continue
                total_lines += file.additions - file.deletions
        user_line_counts[contributer.login] = total_lines

    return user_line_counts



def commit_history_by_repo(owner: str, repo_name: str) -> dict[str, int]: 
    """
    Returns a dict containing the repo name and
    the total number of commits from  the repo 

    """
    g = Github(GITHUB_TOKEN) 
    repo = g.get_repo(f"{owner}/{repo_name}")

    commits = repo.get_commits().totalCount
    return { repo_name: commits }


def commit_history_by_user(owner: str, repo_name: str) -> dict[str, int]: 
    """
    Returns a dict containing the number of commits 
    each user has made from a repo

    {
        user: commit_num, 
        user: commit_num, 
        ...
    }
    """

    user_commits = {}

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{owner}/{repo_name}")

    commits = repo.get_commits() 
    for commit in commits: 
        if commit.author is None: 
            continue

        user = commit.author.login

        if user in user_commits: 
            user_commits[user] += 1
        else: 
            user_commits[user] = 1

    return user_commits




