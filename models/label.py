from enum import Enum


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
    QUESTION = 'question'
    ATTENTION = 'attention'
    PR = 'PR'
    INVALID = 'invalid'
    MERGED = 'merged'
    SYSTEM_DESIGN = 'system design'
    UX = 'UX'
    THIRD_PARTY_ISSUE = '3rd party issue'
    DATA = 'data'
    DUPLICATE = 'duplicate'
    PRIORITY = 'priority'
    BACK_END = 'back-end'
    FRONT_END = 'front-end'
    APP = 'app'

    def __str__(self):
        return self.value
