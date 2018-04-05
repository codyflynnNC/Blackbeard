import kat as kat
import tvmaze as tvmaze
import sqlite as sqlite
from datetime import datetime, timedelta


class Blackbeard:
    def __init__(self):
        self.db_client = sqlite.SQLiteDB()

    def ship(self, show, season, episode):
        self.db_client.insert_show(show, season, episode)
        show_episodes = tvmaze.TvMaze(show).get_show_info()['_embedded']['episodes']
        for e in show_episodes:
            if e['season'] >= season and e['number'] >= episode:
                sid = self.db_client.get_show_id(show)
                a = str(datetime.now() - timedelta(hours=1)) >= '{} {}'.format(e['airdate'], e['airtime'])
                self.db_client.insert_episode(e['name'], e['season'], e['number'], e['airdate'], e['runtime'], 0, a, sid)

    def plunder(self):
        episodes = self.db_client.get_episodes_to_download()
        for e in episodes:
            search_str = '{} S{:02d}E{:02d}'.format(e[4], e[1], e[2])
            if kat.KatTorrents(search_str):
                print('found a torrent and downloaded it!')
                self.db_client.update_episode(e[3])
        print(self.db_client.get_episodes())


if __name__ == '__main__':
    b = Blackbeard()
    b.ship('The Walking Dead', 1, 1)
    b.plunder()