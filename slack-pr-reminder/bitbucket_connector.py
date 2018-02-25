import dateutil.parser
from pybitbucket.auth import OAuth1Authenticator
from pybitbucket.bitbucket import Client
from pybitbucket.pullrequest import PullRequest as BbPullRequest

from models import PullRequest


class BitbucketConnector(object):
    def __init__(self, config):
        self.config = config
        self.bb = Client(OAuth1Authenticator(config['consumer_key'], config['consumer_secret']))

    def get_pull_requests(self):
        pull_requests_by_repo = [self.get_pull_requests_for_repo(repo) for repo in self.config['repositories']]
        pull_requests = [pr for repo in pull_requests_by_repo for pr in repo]
        return pull_requests

    def get_pull_requests_for_repo(self, repo_name):
        owner, name = repo_name.split('/')
        pull_requests = BbPullRequest.find_pullrequests_for_repository_by_state(name, owner)
        full_pull_requests = [BbPullRequest.find_pullrequest_by_id_in_repository(pr.id, name, owner)
                              for pr in pull_requests]
        return [self.convert_pull_request(pr) for pr in full_pull_requests]

    def convert_pull_request(self, pr):
        print(dir(pr))
        reviewers = [r['username'] for r in pr.reviewers]
        created_at = dateutil.parser.parse(pr.created_on)
        return PullRequest(reviewers=reviewers, created_at=created_at, url=pr.links['html']['href'],
                           title=pr.title, creator=pr.author['display_name'], config=self.config)