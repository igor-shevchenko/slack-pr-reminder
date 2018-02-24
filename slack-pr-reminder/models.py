from datetime import datetime
import attr


def get_slack_username(config, user):
    if 'users' in config and user in config['users']:
        return '@' + config['users'][user]
    return user


@attr.s
class PullRequest(object):
    config = attr.ib()
    created_at = attr.ib()
    url = attr.ib()
    title = attr.ib()
    creator = attr.ib()
    reviewers = attr.ib(default=attr.Factory(list))

    def format(self):
        result = '*{2} <{0}|{1}> by _{3}_'.format(self.url, self.title, self.age_emoji, self.creator)

        if self.reviewers:
            reviewers_list = ', '.join(get_slack_username(self.config, r) for r in self.reviewers)
            if len(self.reviewers) == 1:
                result += '. Reviewer: ' + reviewers_list
            else:
                result += '. Reviewers: ' + reviewers_list

        return result

    @property
    def age_emoji(self):
        age = (datetime.now() - self.created_at).days
        if age == 0:
            return ' :new:'
        elif age >= 14:
            return ' :bangbang:'
        elif age >= 7:
            return ' :exclamation:'
        return ''