from github_connection import REPO_LIST
from message import INPUT_CHOOSE_REPO
from message import INPUT_EXPORT_PATH
from message import INPUT_CHOOSE_MILESTONE
from message import INPUT_CONTINUE

repository = {
    'type': 'list',
    'name': 'repo',
    'message': INPUT_CHOOSE_REPO,
    'choices': REPO_LIST
}

export_path = {
    'type': 'input',
    'name': 'export_path',
    'message': INPUT_EXPORT_PATH,
}

continue_work = {
    'type': 'confirm',
    'name': 'continue_work',
    'message': INPUT_CONTINUE
}

_milestone = {
    'type': 'list',
    'name': 'milestone',
    'message': INPUT_CHOOSE_MILESTONE,
    'choices': []
}


def build_milestone(milestone_list):
    # initialize and add all
    _milestone['choices'] = ['all'] + milestone_list
    return _milestone
