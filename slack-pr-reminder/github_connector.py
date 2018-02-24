from github import Github


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
        return list(pull_requests)