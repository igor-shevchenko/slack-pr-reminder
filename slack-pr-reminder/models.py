import attr

@attr.s
class PullRequest(object):
    created_at = attr.ib()
    url = attr.ib()
    title = attr.ib()
    creator = attr.ib()
    reviewers = attr.ib(default=attr.Factory(list))