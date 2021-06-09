import sys

import message

from github_connection import REPO_LIST
from github_connection import GithubConnection


def run_crawler():
    path = input(message.INPUT_EXPORT_FOLDER)
    print(message.INPUT_CHOOSE_REPO)
    for i, repo in enumerate(REPO_LIST):
        print(f'{i} : {repo}')
    try:
        repo_num = int(input())
    except ValueError as e:
        print(message.ERROR_INPUT_EXIT)
        sys.exit(e)
    repo_name = REPO_LIST[repo_num]
    try:
        repo = GithubConnection(name=repo_name)
    except GithubConnection.LoginError:
        print(message.ERROR_LOGIN)
        sys.exit()
    try:
        repo.export_csv()
    except GithubConnection.ConnectionError:
        print(message.ERROR_CONNECTION)
        sys.exit()


if __name__ == '__main__':
    run_crawler()
