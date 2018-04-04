import kat as kat
import airdates as ad


class Pirate:
    def __init__(self, show, starting_episode, sid):
        self.show = show
        self.starting_episode = starting_episode
        self.show_id = sid

    def inc_episode(self):
        """
        :return: the next episode string
        """
        return '{}{}'.format(self.starting_episode[:4], '{:02d}'.format(int(self.starting_episode[4:]) + 1))

    def inc_season(self):
        """
        :return: the next season string
        """
        return 'S{}{}'.format('{:02d}'.format(int(self.starting_episode[1:3]) + 1), self.starting_episode[3:])

    @staticmethod
    def pirate_episode(episode):
        k = kat.KatTorrents(episode)
        k.


if __name__ == '__main__':
    p = Pirate('Sneaky Pete', 'S01E01', 3062)
    next_episode = p.inc_episode()
    next_season = p.inc_season()
    print(next_episode)
