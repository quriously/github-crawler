import os
import requests
import datetime
import csv

from enum import Enum


REPO_OWNER = os.environ.get('OWNER')
REPO_LIST = ['airklass', 'airklass-ios', 'airklass-android']

ISSUE_URL = 'https://api.github.com/repos/{owner}/{repo}/issues?page={page}'
USER = os.environ.get('USER')
TOKEN = os.environ.get('TOKEN')
EXPORT_FILE_NAME = 'issue_list_{now}_{sort_kind}.csv'
EXPORT_PATH = f'/Users/hyunwoo/Desktop/{EXPORT_FILE_NAME}'
CSV_ENCODING = 'utf-8'


class GithubConnection:
    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.session.auth = (USER, TOKEN)
        self.name = kwargs.get('name')
        self.owner = REPO_OWNER
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
class Issue:
    def __init__(self, **kwargs):
        url = kwargs.get('url')
        repository_url = kwargs.get('repository_url')
        labels_url = kwargs.get('labels_url')
        comments_url = kwargs.get('comments_url')
        events_url = kwargs.get('events_url')
        html_url = kwargs.get('html_url')
        issue_id = kwargs.get('id')
        node_id = kwargs.get('node_id')
        number = kwargs.get('number')
        title = kwargs.get('title')
        user = kwargs.get('user').get('login') if kwargs.get('user') else None
        labels = Issue._parse_labels(kwargs.get('labels'))
        state = kwargs.get('state')
        locked = kwargs.get('locked')
        assignee = kwargs.get('assignee')
        assignees = Issue._parse_assignee(kwargs.get('assignees'))
        milestone = kwargs.get('milestone')
        comments = kwargs.get('comments')
        created_at = kwargs.get('created_at')
        updated_at = kwargs.get('updated_at')
        closed_at = kwargs.get('closed_at')

    @staticmethod
    def _parse_labels(input_labels):
        label_list = []
        for input_label in input_labels:
            label_name = input_label.get('name')
            label = Label(label_name)
            label_list.append(label)
        return label_list

    @staticmethod
    def _parse_assignee(input_assignees):
        return [assignee.login for assignee in input_assignees]


class Label(Enum):
    BUG = 'bug'
    ENHANCEMENT = 'enhancement'
    IN_TESTING = 'in-testing'
    TESTED = 'tested'
    UNRESOLVED = 'unresolved'
    WONTFIX = 'wontfix'
    NEED_WORK = 'need-work'
    DESIGN = 'design'
    SUGGESTION = 'suggestion'

