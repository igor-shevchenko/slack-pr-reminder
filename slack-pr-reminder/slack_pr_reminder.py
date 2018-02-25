import requests
import yaml

from github_connector import GitHubConnector
from bitbucket_connector import BitbucketConnector

with open('config.yaml') as f:
    config = yaml.load(f)


def format_message(pull_requests):
    count = len(pull_requests)
    if count == 1:
        msg = 'There is *1* pull request waiting for review: '
    else:
        msg = 'There are *' + str(count) + '* pull requests waiting for review: '
    msg += '\n\n'
    msg += '\n'.join(pr.format() for pr in pull_requests)
    return msg

def send_to_slack(message):
    payload = {
        'text': message,
        'icon_emoji': ':mailbox_with_mail:',
        'username': 'Pull Request Reminder',
        'link_names': '1'
    }
    response = requests.post(config['slack_webhook_url'], json=payload)


def send_reminder():
    pull_requests = []

    if 'github' in config:
        connector = GitHubConnector(config['github'])
        pull_requests += connector.get_pull_requests()
    if 'bitbucket' in config:
        connector = BitbucketConnector(config['bitbucket'])
        pull_requests += connector.get_pull_requests()

    if not pull_requests:
        return

    message = format_message(pull_requests)
    print(message)
    send_to_slack(message)


if __name__ == '__main__':
    send_reminder()