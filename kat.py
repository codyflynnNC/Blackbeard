import urllib.parse
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


class KatTorrents:
    """
    Base class for KatTorrents script
    """

    def __init__(self, search):
        """
        Init KatTorrents class

        @type  search: str
        @param search: Search string provided by user
        """
        url_base = 'https://kat.rip/usearch/'
        url_base += urllib.parse.quote_plus(search)
        url_sort = '/?field=seeders&sorder=desc'
        self.url = url_base + url_sort
        self._run_search()

    def _run_search(self):
        """
        Execute the search against kat.rip using the generated search string in self.url

        @rtype: string
        @return: The source of the search page
        """
        try:
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            q = Request(self.url)
            q.add_header('User-Agent', user_agent)
            a = urlopen(q)
            soup = BeautifulSoup(a, "html.parser").find('table', id='mainSearchTable').find('table', class_='data')
            torrent_files = soup.find_all('tr', class_=['odd', 'even'])
            if torrent_files:
                self.download_torrent(self.get_best_torrent(torrent_files))
        except Exception as e:
            print('No torrent found!\n, error: %s' % e)

    @staticmethod
    def get_best_torrent(t):
        for torrent in t:
            file_size = human_readable_to_bytes(torrent.find('td', class_='nobr').text)
            seeders = int(torrent.find('td', class_='green').text)
            if 1000000000 <= file_size[0] <= 2000000000 and seeders >= 50:
                print('file size larger than 1 gb and less than 2gb with %s seeders > 50' % seeders)
                return torrent.td.div.find('a', title='Torrent magnet link').attrs['href']

    @staticmethod
    def download_torrent(mag):
        try:
            os.startfile(mag)
        except Exception as e:
            raise e


def human_readable_to_bytes(size):
    """Given a human-readable byte string (e.g. 2G, 10GB, 30MB, 20KB),
       return the number of bytes.  Will return 0 if the argument has
       unexpected form.
    """
    if size[-1] == 'B':
        size = size[:-1]
    if size.isdigit():
        b = int(size)
    else:
        b = str(int(float(size[:-1])))
        unit = size[-1]
        if b.isdigit():
            b = int(b)
            if unit == 'G':
                b *= 1073741824
            elif unit == 'M':
                b *= 1048576
            elif unit == 'K':
                b *= 1024
            else:
                b = 0
        else:
            b = 0
    return b, size + 'B'


if __name__ == '__main__':
    kat = KatTorrents('walking dead')
    torrents = kat.run_search()
    if torrents:
        magnet_link = kat.get_best_torrent(torrents)
        kat.download_torrent(magnet_link)
    else:
        # check if episode is available via airdates
        pass
