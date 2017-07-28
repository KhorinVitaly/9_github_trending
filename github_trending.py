import requests
from datetime import datetime


def get_seven_days_ago_date():
    current_date = datetime.today()
    current_timestamp = current_date.timestamp()
    return datetime.fromtimestamp(current_timestamp - (86400 * 7)).date()


def get_trending_repositories(top_size):
    isoformat_date = get_seven_days_ago_date.isoformat()
    search_parameters = {'q': 'created:>{0}'.format(isoformat_date),
                         'sort': 'stars',
                         'order': 'desc'}
    response = requests.get('https://api.github.com/search/repositories', search_parameters)
    result_as_json = response.json()
    return result_as_json['items'][:top_size]


def get_open_issues_info(repo_owner, repo_name):
    url = 'https://api.github.com/repos/{0}/{1}/issues'.format(repo_owner, repo_name)
    response = requests.get(url, {'state': 'open'})
    result_as_json = response.json()
    if response.status_code == 200:
        return ', Open issues amount: {0}'.format(len(result_as_json))
    else:
        return ', Issues count failed: {0}'.format(result_as_json['message'])


if __name__ == '__main__':
    top_size = 20
    try:
        repositories = get_trending_repositories(top_size)
        for repo in repositories:
            repo_url = repo['html_url']
            open_issues_info = get_open_issues_info(repo['owner']['login'], repo['name'])
            print('{0}{1}'.format(repo_url, open_issues_info))
    except requests.HTTPError as error:
        print('HTTP Error')
        print('Response is: {0}'.format(error.response.content))
    except requests.ConnectionError:
        print('Connection failed')

