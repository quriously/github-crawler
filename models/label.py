from enum import Enum


class Label(Enum):
    BUG = 'bug'
    ENHANCEMENT = 'enhancement'
    IN_TESTING = 'in-testing'
    TESTED = 'tested'
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
    THIRD_PARTY = '3rd party'
    DATA = 'data'
    DUPLICATE = 'duplicate'
    PRIORITY = 'priority'
    BACK_END = 'back-end'
    FRONT_END = 'front-end'
    APP = 'app'
    FIXED = 'fixed'
    RESOLVED = 'resolved'
    UNRESOLVED = 'unresolved'

    def __str__(self):
        return self.value
