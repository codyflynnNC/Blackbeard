import urllib.parse
import zlib
import os
from subprocess import call
import sys
from urllib.request import Request, urlopen  # Python 3
from bs4 import BeautifulSoup
import requests
import re


class Airdates:
    def __init__(self, show, starting_episode, show_id=None):
        self.url = 'http://www.airdates.tv/s?q='
        self.starting_episode = starting_episode
        self.show = show
        self.show_id = show_id

    def get_show_id(self):
        r = requests.get('{}{}'.format(self.url, urllib.parse.quote_plus(self.show)))
        soup = BeautifulSoup(r.text, "html.parser").find('ul')
        for item in soup.children:
            if item != '\n':
                show_name = item.find('b').text
                if show_name == self.show:
                    self.show_id = re.sub(r"\D", "", item.find_all('a')[1].attrs['href'])

    def get_show_episodes(self):
        q_string = urllib.parse.quote_plus('info:{}'.format(self.show_id))
        r = requests.get('{}{}'.format(self.url, q_string))
        soup = BeautifulSoup(r.content, "html.parser")
        return soup


if __name__ == '__main__':
    airdates = Airdates('the walking dead', 's01e01', 754)
    #airdates.get_show_id()
    airdates.get_show_episodes()
