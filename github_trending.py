import requests
from datetime import datetime, timedelta


def get_past_date(count_of_day_ago):
    current_date = datetime.today().date()
    return current_date - timedelta(days=count_of_day_ago)


def get_trending_repositories(top_size):
    count_of_day_ago = 7
    iso_format_date = get_past_date(count_of_day_ago).isoformat()
    search_parameters = {'q': 'created:>{0}'.format(iso_format_date),
                         'sort': 'stars',
                         'order': 'desc',
                         'page': '1',
                         'per_page': str(top_size)}
    response = requests.get('https://api.github.com/search/repositories', search_parameters)
    result_as_json = response.json()
    return result_as_json['items']


if __name__ == '__main__':
    top_size = 20
    try:
        repositories = get_trending_repositories(top_size)
        print(len(repositories))
        for repo in repositories:
            repo_url = repo['html_url']
            open_issues_count = repo['open_issues_count']
            print('{0}, open issues count: {1}'.format(repo_url, open_issues_count))
    except requests.HTTPError as error:
        print('HTTP Error')
        print('Response is: {0}'.format(error.response.content))
    except requests.ConnectionError:
        print('Connection failed')

