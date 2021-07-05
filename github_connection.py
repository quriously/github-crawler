import os
import requests
import datetime
import csv

from label import Label
from message import INFO_CRAWLING_LOADING
from message import INFO_CRAWLING_FINISHED
from message import ERROR_LABEL_NOT_FOUND

REPO_OWNER = os.environ.get('OWNER')
REPO_LIST = ['airklass', 'airklass-ios', 'airklass-android']

ISSUE_URL = 'https://api.github.com/repos/{owner}/{repo}/issues?page={page}'
USER = os.environ.get('USER')
TOKEN = os.environ.get('TOKEN')
EXPORT_FILE_NAME = 'issue_list_{now}_{sort_kind}.csv'
CSV_ENCODING = 'utf-8'
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

    class LoginError(Exception):
        pass

    class ConnectionError(Exception):
        pass

    def export_csv(self, path='', sort_kind='all', sorted_list=None):
        if not os.path.exists(path):
            os.makedirs(path)
        sorted_list = sorted_list if sorted_list else self.issue_list
        now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        file_name = EXPORT_FILE_NAME.format(now=now, sort_kind=sort_kind)
        export_file = os.path.join(path, file_name)
        with open(export_file, 'w', newline='', encoding=CSV_ENCODING) as f:
            writer = csv.DictWriter(f, fieldnames=Issue.get_column_list(choose=True))
            writer.writeheader()
            for issue in sorted_list:
                writer.writerow(issue.get_choose_dict())


class Issue:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.repository_url = kwargs.get('repository_url')
        self.labels_url = kwargs.get('labels_url')
        self.comments_url = kwargs.get('comments_url')
        self.events_url = kwargs.get('events_url')
        self.html_url = kwargs.get('html_url')
        self.issue_id = kwargs.get('id')
        self.node_id = kwargs.get('node_id')
        self.number = kwargs.get('number')
        self.title = kwargs.get('title')
        # author
        self.user = kwargs.get('user').get('login') if kwargs.get('user') else None
        self.labels = Issue._parse_labels(kwargs.get('labels'))
        self.state = kwargs.get('state')
        self.locked = kwargs.get('locked')
        self.assignee = kwargs.get('assignee')
        self.assignees = Issue._parse_assignee(kwargs.get('assignees'))
        self.milestone = kwargs.get('milestone')
        self.comments = kwargs.get('comments')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        self.closed_at = kwargs.get('closed_at')

    @staticmethod
    def _parse_labels(input_labels):
        label_list = []
        if not input_labels:
            return label_list
        for input_label in input_labels:
            label_name = input_label.get('name')
            try:
                label = Label(label_name)
            except ValueError as e:
                print(ERROR_LABEL_NOT_FOUND)
                print(e)
                continue
            label_list.append(label)
        return label_list

    @staticmethod
    def _parse_assignee(input_assignees):
        if not input_assignees:
            return []
        return [assignee.get('login') for assignee in input_assignees]

    @classmethod
    def generate_issue_list(cls, issue_list):
        result_list = []
        for issue_dict in issue_list:
            issue = cls(**issue_dict)
            result_list.append(issue)
        return result_list

    @classmethod
    def get_column_list(cls, choose=False):
        if choose:
            return ['number', 'title', 'labels', 'user', 'assignees', 'html_url', 'created_at', 'closed_at']
        to_dict = vars(cls())
        to_keys = to_dict.keys()
        return list(to_keys)

    def get_choose_dict(self):
        all_dict = vars(self)
        result = {}
        column_list = Issue.get_column_list(choose=True)
        try:
            for key in all_dict.keys():
                if key not in column_list:
                    continue
                result[key] = all_dict.get(key)
        except ValueError as e:
            print(e)
        return result
