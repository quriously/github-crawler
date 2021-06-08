import os
import requests
import datetime
import csv


REPO_OWNER = os.environ.get('OWNER')
REPO_LIST = ['airklass', 'airklass-ios', 'airklass-android']
LABEL_LIST = ['bug', 'enhancement', 'in-testing', 'tested', 'unresolved', 'wontfix', 'need-work', 'design',
              'suggestion']
ISSUE_URL = 'https://api.github.com/repos/{owner}/{repo}/issues?page={page}'
USER = os.environ.get('USER')
TOKEN = os.environ.get('TOKEN')
EXPORT_FILE_NAME = 'issue_list_{now}_{sort_kind}.csv'
EXPORT_PATH = f'/Users/hyunwoo/Desktop/{EXPORT_FILE_NAME}'
CSV_ENCODING = 'utf-8'


class GithubConnection:
    def __init__(self, **kwargs):
        self.user = kwargs.get('user', USER)
        self.token = kwargs.get('token', TOKEN)
        self.session = requests.Session()
        self.session.auth = (self.user, self.token)


class GithubRepo(GithubConnection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name')
        self.owner = kwargs.get('owner', REPO_OWNER)
        self._max_page = None
        self._issue_list = []

    @property
    def max_page(self):
        if self._max_page:
            return self._max_page
        self._max_page = self._check_max_page()
        return self._max_page

    @property
    def issue_list(self, refresh=False):
        if self._issue_list and not refresh:
            return self._issue_list
        self._issue_list = self._crawling_issue_list()
        return self._issue_list

    def _check_max_page(self, page=0):
        step_page = page + 1
        page_url = ISSUE_URL.format(owner=self.owner, repo=self.name, page=step_page)

        with self.session.get(page_url) as s:
            sources = s.json()
        if not len(sources):
            return page
        return self._check_max_page(page=step_page)

    def _crawling_issue_list(self, crawling_list=None, page=0):
        crawling_list = crawling_list if crawling_list else []
        step_page = page + 1
        if step_page > self.max_page:
            return crawling_list
        page_url = ISSUE_URL.format(owner=self.owner, repo=self.name, page=step_page)
        with self.session.get(page_url) as s:
            sources = s.json()
        crawling_list.extend(sources)
        return self._crawling_issue_list(crawling_list=crawling_list, page=step_page)

    def export_csv(self, sort_kind='', sorted_list=None):
        sorted_list = sorted_list if sorted_list else self._issue_list
        now = datetime.datetime.now().strftime('%Y_%m_%d%_%H_%M_%S')
        export_file = EXPORT_PATH.format(now=now, sort_kind=sort_kind)
        with open(export_file, 'w', newline='', encoding=CSV_ENCODING) as f:
            writer = csv.writer(f)

