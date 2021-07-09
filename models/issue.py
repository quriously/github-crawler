from label import Label
from message import ERROR_LABEL_NOT_FOUND


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
