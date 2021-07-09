import sys

from PyInquirer import prompt

from github_connection import GithubConnection
from message import ERROR_LOGIN
from message import ERROR_CONNECTION
from message import INFO_COMPLETE
from message import INFO_EXIT
from utils import export_csv
from question import repository
from question import export_path
from question import continue_work
from question import build_milestone


repository_dict = {}
answer_export_path = ''


def get_repo(repo_name):
    repo = repository_dict.get(repo_name)
    if repo:
        return repo
    try:
        repo = GithubConnection(name=repo_name)
    except GithubConnection.LoginError:
        print(ERROR_LOGIN)
        sys.exit()
    repository_dict[repo_name] = repo
    return repo


def run_crawler():
    answer_repo = prompt([repository]).get('repo')
    repo = get_repo(answer_repo)
    question_milestone = build_milestone(repo.get_milestone_title_list())
    answer_milestone = prompt([question_milestone]).get('milestone')
    export_list = repo.issue_list
    if answer_milestone != 'all':
        export_list = repo.filter_milestone(answer_milestone)
    try:
        export_csv(issue_list=export_list, dest_path=answer_export_path, repo_name=answer_repo,
                   extra_name=answer_milestone)
    except GithubConnection.ConnectionError:
        print(ERROR_CONNECTION)
        sys.exit()


if __name__ == '__main__':
    answer_export_path = prompt([export_path]).get('export_path')
    while True:
        run_crawler()
        print(INFO_COMPLETE)
        answer_continue = prompt([continue_work]).get('continue_work')
        if not answer_continue:
            break
    print(INFO_EXIT)
