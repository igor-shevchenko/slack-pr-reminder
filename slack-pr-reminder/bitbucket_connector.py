import dateutil.parser
from pybitbucket.auth import OAuth1Authenticator
from pybitbucket.bitbucket import Client
from pybitbucket.pullrequest import PullRequest as BbPullRequest
from pybitbucket.repository import Repository

from models import PullRequest


class BitbucketConnector(object):
    def __init__(self, config):
        self.config = config
        self.bb = Client(OAuth1Authenticator(config['consumer_key'], config['consumer_secret']))

    def get_pull_requests(self):
        repos = self.config.get('repositories', [])

        if 'organization' in self.config:
            repos += self.get_repos_for_organization(self.config['organization'])

        pull_requests_by_repo = [self.get_pull_requests_for_repo(repo) for repo in repos]
        pull_requests = [pr for repo in pull_requests_by_repo for pr in repo]
        return pull_requests

    def get_repos_for_organization(self, name):
        repos = list(Repository.find_repositories_by_owner_and_role(name, 'member', self.bb))

        if not len(repos) or not isinstance(repos [0], Repository):
            return []

        return [r.full_name for r in repos]

    def get_pull_requests_for_repo(self, repo_name):
        owner, name = repo_name.split('/')
        pull_requests = list(BbPullRequest.find_pullrequests_for_repository_by_state(name, owner, client=self.bb))

        if not len(pull_requests) or not isinstance(pull_requests[0], BbPullRequest):
            return []

        full_pull_requests = [BbPullRequest.find_pullrequest_by_id_in_repository(pr.id, name, owner, self.bb)
                              for pr in pull_requests]
        return [self.convert_pull_request(pr) for pr in full_pull_requests]

    def convert_pull_request(self, pr):
        reviewers = [r.username for r in pr.reviewers]
        created_at = dateutil.parser.parse(pr.created_on)
        return PullRequest(reviewers=reviewers, created_at=created_at, url=pr.links['html']['href'],
                           title=pr.title, creator=pr.author.display_name, config=self.config)