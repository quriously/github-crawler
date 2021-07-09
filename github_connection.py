import os
import requests

from models import Issue
from models import Milestone
from message import INFO_CRAWLING_LOADING
from message import INFO_CRAWLING_FINISHED

REPO_OWNER = os.environ.get('OWNER')
REPO_LIST = ['airklass', 'airklass-ios', 'airklass-android']

ISSUE_URL = 'https://api.github.com/repos/{owner}/{repo}/issues?page={page}'
MILESTONE_URL = 'https://api.github.com/repos/{owner}/{repo}/milestones'
USER = os.environ.get('USER')
TOKEN = os.environ.get('TOKEN')
COLUMN = ['No.', 'Title', 'Label status', 'github No.', 'URL']


class GithubConnection:
    def __init__(self, **kwargs):
        self.session = requests.Session()
        if not USER or not TOKEN:
            raise GithubConnection.LoginError()
        self.session.auth = (USER, TOKEN)
        self.name = kwargs.get('name')
        self.owner = REPO_OWNER
        self.max_page = None
        self.issue_list = self._crawling_issue_list()
        self.milestone_list = self._crawling_milestone_list()

    def _crawling_issue_list(self, crawling_list=None, page=0):
        crawling_list = crawling_list if crawling_list else []
        step_page = page + 1
        print(INFO_CRAWLING_LOADING.format(page=step_page))
        page_url = ISSUE_URL.format(owner=self.owner, repo=self.name, page=step_page)
        with self.session.get(page_url) as s:
            if s.status_code != 200:
                raise GithubConnection.ConnectionError()
            source_list = s.json()
        if not len(source_list):
            self.max_page = page
            print(INFO_CRAWLING_FINISHED.format(max_page=self.max_page))
            return crawling_list
        sources = Issue.generate_issue_list(source_list)
        crawling_list.extend(sources)
        return self._crawling_issue_list(crawling_list=crawling_list, page=step_page)

    def _crawling_milestone_list(self):
        url = MILESTONE_URL.format(owner=self.owner, repo=self.name)
        with self.session.get(url) as s:
            if s.status_code != 200:
                raise GithubConnection.ConnectionError()
            source_list = s.json()
        return Milestone.bulk_generate(source_list)

    def filter_milestone(self, milestone_title):
        result_list = []
        for issue in self.issue_list:
            if not issue.milestone:
                continue
            if issue.milestone.get('title') != milestone_title:
                continue
            result_list.append(issue)
        return result_list

    def get_milestone_title_list(self):
        return [m.title for m in self.milestone_list]

    class LoginError(Exception):
        pass

    class ConnectionError(Exception):
        pass
