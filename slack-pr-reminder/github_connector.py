from github import Github

from models import PullRequest

class GitHubConnector(object):
    def __init__(self, config):
        self.config = config
        self.github = Github(config['github_access_token'])

    def get_pull_requests(self):
        pull_requests_by_repo = [self.get_pull_requests_for_repo(repo) for repo in self.config['repositories']]
        pull_requests = [pr for repo in pull_requests_by_repo for pr in repo]
        return pull_requests

    def get_pull_requests_for_repo(self, repo_name):
        repo = self.github.get_repo(repo_name)
        pull_requests = repo.get_pulls()
        return [self.convert_pull_request(pr) for pr in pull_requests]

    def convert_pull_request(self, pr):
        reviewers = [r.login for r in pr.get_reviewer_requests()]
        return PullRequest(reviewers=reviewers, created_at=pr.created_at, url=pr.html_url,
                           title=pr.title, creator=pr.user.name)