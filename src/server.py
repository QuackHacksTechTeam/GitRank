

"""
REST API for github repo data
Essentially just a wrapper around the github api, to be used with a data displaying 
frontend

"""

from flask import Flask, jsonify, send_from_directory
import os
from dotenv import load_dotenv

from gh_requests import requests
from utils.repo_url_reader import read_urls, parse_urls


#---------------------------------------------------
load_dotenv()
FRONTEND_PATH = "../frontend/build"
app = Flask(__name__, static_folder=FRONTEND_PATH + '/static', static_url_path='/static')

PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "localhost")

REPO_TEXT_FILE = "../repos.txt"
# A list of tuples, containing owner, repo 
OWNERS_REPOS = parse_urls(read_urls(REPO_TEXT_FILE))
print(f"Using repos: {OWNERS_REPOS}...")
# ---------------------------------------------------


# Send all unknown paths to the root 
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    return send_from_directory(os.path.join(app.root_path, FRONTEND_PATH), 'index.html')


# ----------------------- API --------------------------

@app.route('/api/repo-loc', methods=["GET"])
def get_repo_lines_of_code(): 
    """
    Sends a list of all repos with their total lines of code

    In the JSON form 
    [
        {
            repo_name: string, 
            lines_of_code: number
        }
        ...
    ]
    """
    all_repo_loc = {}
    for owner, reponame in OWNERS_REPOS: 
        try: 
            repo_loc = requests.lines_of_code_by_repo(owner, reponame)
            all_repo_loc.update(repo_loc)

        except Exception as error: 
            return jsonify({ "Error": str(error) }), 500

    all_user_commit_labeled = [{"repo_name": user, "lines_of_code": count} for user, count in all_repo_loc.items()]
    return jsonify(all_user_commit_labeled)


@app.route('/api/user-loc', methods=["GET"])
def get_user_lines_of_code(): 
    """
    Sends a list of all users from a repo with their total contributed lines of code

    In the JSON form 
    [
        {
            username: string, 
            lines_of_code: number
        }
        ...
    ]

    """
    all_user_lines_of_code = {}

    for owner, reponame in OWNERS_REPOS: 
        try: 
            users_lines_of_code = requests.lines_of_code_by_user(owner, reponame)
            print(f"Found {users_lines_of_code}")
            for user, lines_of_code in users_lines_of_code.items(): 
                if user not in all_user_lines_of_code: 
                    all_user_lines_of_code[user] = lines_of_code 
                else: 
                    all_user_lines_of_code[user] += lines_of_code 

        except Exception as error:  
            return jsonify({ "Error": str(error) }), 500

    all_user_commit_labeled = [{"username": user, "lines_of_code": count} for user, count in all_user_lines_of_code.items()]
    return jsonify(all_user_commit_labeled)




@app.route('/api/repo-commits', methods=["GET"])
def get_repo_commits(): 
    """
    Send all repo commit history in json in the form 

    [
        {
            repo_name: string, 
            commits: int 
        }
        ...
    ]
    """
    all_repo_commits = []
    for owner, reponame in OWNERS_REPOS: 
        try: 
            repo_commits = requests.commit_history_by_repo(owner, reponame)
            all_repo_commits.append(repo_commits)

        except Exception: 
            return jsonify({ "Error": "Invalid GitHub API request" }), 500

    all_repo_commits_labeld = [{"repo_name": list(item.keys())[0], "commits": list(item.values())[0]} for item in all_repo_commits]
    
    return jsonify(all_repo_commits_labeld)
        

    


@app.route('/api/user-commits', methods=['GET'])
def get_user_commits(): 
    """
    Send all user commit history in json in the form 

    [
        {
            username: string, 
            commits: int 
        }
        ...
    ]

    """

    all_user_commits = {}
    for owner, reponame in OWNERS_REPOS: 

        # Try to append all users commits to the overall dict 
        try: 
            users_commit_history = requests.commit_history_by_user(owner, reponame)
            for user, num_commits in users_commit_history.items(): 
                if user not in all_user_commits: 
                    all_user_commits[user] = num_commits
                else: 
                    all_user_commits[user] += num_commits

        except Exception:  
            return jsonify({ "Error": "Invalid GitHub API request" }), 500

    all_user_commit_labeled = [{"username": user, "commits": count} for user, count in all_user_commits.items()]
    return jsonify(all_user_commit_labeled)


if __name__ == "__main__": 
    app.run(host=HOST, port=PORT, debug=True)















    



