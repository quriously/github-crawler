import os
import csv
import datetime

from issue import Issue

EXPORT_FILE_NAME = 'issue_list_{now}_{repo_name}_{extra_name}.csv'
CSV_ENCODING = 'utf-8'


def export_csv(issue_list=None, **kwargs):
    dest_path = kwargs.get('dest_path')
    repo_name = kwargs.get('repo_name', '')
    extra_name = kwargs.get('extra_name', '')
    if not dest_path:
        raise Exception()
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    file_name = EXPORT_FILE_NAME.format(now=now, repo_name=repo_name, extra_name=extra_name)
    export_file = os.path.join(dest_path, file_name)
    with open(export_file, 'w', newline='', encoding=CSV_ENCODING) as f:
        writer = csv.DictWriter(f, fieldnames=Issue.get_column_list(choose=True))
        writer.writeheader()
        for issue in issue_list:
            writer.writerow(issue.get_choose_dict())
