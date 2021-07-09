

class Milestone:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        open_issues = kwargs.get('open_issues')
        closed_issues = kwargs.get('closed_issues')
        state = kwargs.get('state')

    @classmethod
    def bulk_generate(cls, creature_list):
        obj_list = []
        for creature in creature_list:
            obj = cls(**creature)
            obj_list.append(obj)
        return obj_list
