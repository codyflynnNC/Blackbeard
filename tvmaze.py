import requests
import urllib.parse
import json


class TvMaze:
    """
    Gets all important information about a show
    """
    def __init__(self, show):
        self.api_root_url = 'http://api.tvmaze.com'
        self.show = show

    def get_show_info(self):
        proxies = {
            'http': 'one.proxy.att.com:8080'
        }
        q = '/singlesearch/shows?q={}&embed=episodes'.format(urllib.parse.quote_plus(self.show))
        r = requests.get('{}{}'.format(self.api_root_url, q))
        return json.loads(r.text)


if __name__ == '__main__':
    tvmaze = TvMaze('hate thy neighbor')
    info = tvmaze.get_show_info()
    episodes = info['_embedded']['episodes']
