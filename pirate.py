import kat as kat
import tvmaze as tvmaze
import sqlite as sqlite
from datetime import datetime, timedelta
import logging

logging.basicConfig(format='%(asctime)s %(message)s', filename='log.log', level=logging.DEBUG)


class Blackbeard:
    def __init__(self):
        self.db_client = sqlite.SQLiteDB()

    def ship(self, show, season, episode):
        self.db_client.insert_show(show, season, episode)
        show_episodes = tvmaze.TvMaze(show).get_show_info()['_embedded']['episodes']
        for e in show_episodes:
            if e['season'] >= season and e['number'] >= episode:
                sid = self.db_client.get_show_id(show)
                airtime = '{} {}'.format(e['airdate'], e['airtime'])
                a = str(datetime.now() - timedelta(hours=1)) >= '{}'.format(airtime)
                self.db_client.insert_episode(e['name'], e['season'], e['number'], airtime, e['runtime'], 0, a, sid)

    def update(self):
        shows = self.db_client.get_shows()
        for s in shows:
            show_episodes = tvmaze.TvMaze(s[1]).get_show_info()['_embedded']['episodes']
            diff = len(show_episodes) - len(self.db_client.get_episodes_for_show(s[0]))
            if diff > 0:
                # found new episodes that are not in the db, need to insert the new ones
                for e in show_episodes:
                    e_uid = '{}_{}_S{}E{}'.format(s[0], e['name'], e['season'], e['number'])
                    if not self.db_client.is_episode_exist(e_uid):
                        airtime = '{} {}'.format(e['airdate'], e['airtime'])
                        a = str(datetime.now() - timedelta(hours=1)) >= '{}'.format(airtime)
                        self.db_client.insert_episode(e['name'], e['season'], e['number'], airtime, e['runtime'], 0, a, s[0])
        logging.info('updating available episodes..')
        # e[6] = downloaded, 4=airdate, 5=runtime, 8=e_uid
        episodes = self.db_client.get_all_episodes()
        for e in episodes:
            logging.info('checking episode: {}'.format(e[8]))
            if not e[6] and not e[7]:
                current_time = str(datetime.now())
                if current_time > '{} {}'.format(e[4], e[5]):
                    logging.info('marking episode {} as available..'.format(e[8]))
                    self.db_client.make_episode_available(e[8])

    def plunder(self):
        logging.info('checking for plunder')
        episodes = self.db_client.get_episodes_to_download()
        for e in episodes:
            logging.info('episode {} is marked for download'.format(e[3]))
            search_str = '{} S{:02d}E{:02d}'.format(e[4], e[1], e[2])
            started_download = kat.KatTorrents(search_str).run_search()
            if started_download:
                logging.info('downloading episode {}'.format(e[3]))
                self.db_client.update_episode(e[3])


if __name__ == '__main__':
    logging.info('Starting Blackbeard...')
    b = Blackbeard()
    b.update()
    b.plunder()
    logging.info('Ending Blackbeard')
