import sys

from github_connection import REPO_LIST
from github_connection import GithubConnection
from message import INPUT_EXPORT_FOLDER
from message import INPUT_CHOOSE_REPO
from message import ERROR_INPUT_EXIT
from message import ERROR_LOGIN
from message import ERROR_CONNECTION


def run_crawler():
    path = input(INPUT_EXPORT_FOLDER)
    print(INPUT_CHOOSE_REPO)
    for i, repo in enumerate(REPO_LIST):
        print(f'{i} : {repo}')
    try:
        repo_num = int(input())
    except ValueError as e:
        print(ERROR_INPUT_EXIT)
        sys.exit(e)
    repo_name = REPO_LIST[repo_num]
    try:
        repo = GithubConnection(name=repo_name)
    except GithubConnection.LoginError:
        print(ERROR_LOGIN)
        sys.exit()
    try:
        repo.export_csv(path=path)
    except GithubConnection.ConnectionError:
        print(ERROR_CONNECTION)
        sys.exit()


if __name__ == '__main__':
    run_crawler()
