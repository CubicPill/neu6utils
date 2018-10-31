#!/usr/bin/env python3

import os
import random
import sys
import time

import requests
from bs4 import BeautifulSoup

from utils import dump_cookies, NotLoggedIn, load_cookies, test_session, login


class Worker:

    def __init__(self, session):
        self._session = session
        dump_cookies(self._session.cookies.get_dict(), 'cookies.json')

    def find_all_forums(self):
        url = 'http://bt.neu6.edu.cn/forum.php'
        response = self._session.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        forum_urls = [td.find('dt').find('a')['href'] for td in soup.find_all('td', {'class': 'fl_g'})]
        return ['http://bt.neu6.edu.cn/' + url for url in forum_urls][5:-9]
        # get rid of the non-resource forums

    def random_access_post(self, form_url):
        response = self._session.get(form_url, allow_redirects=False)
        if response.status_code != 200:
            raise NotLoggedIn
        soup = BeautifulSoup(response.content, 'html5lib')
        post_urls = ['http://bt.neu6.edu.cn/' + td.find('a', {'class': 'xst'})['href'] for td in
                     soup.find_all('th', {'class': ['new', 'common']})]
        if not post_urls or len(post_urls) == 0:
            return None
        response = self._session.get(random.choice(post_urls))
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup.find('title').text

    def keep_online(self):
        forums = self.find_all_forums()
        return self.random_access_post(random.choice(forums))


if __name__ == '__main__':
    try:
        if os.path.isfile('cookies.json'):
            print('Cookies found.')
            cookies = load_cookies('cookies.json')
            session = requests.session()
            for _k, _v in cookies.items():
                session.cookies.set(_k, _v)
            if test_session(session):
                print('Logged in using cookies')
            else:
                print('Invalid cookies!')
                raise NotLoggedIn
        else:
            raise NotLoggedIn
    except NotLoggedIn:
        if len(sys.argv) != 3:
            print('You need to provide your credentials.')
            print('Usage: python3 ' + sys.argv[0] + ' <username> <password>')
            sys.exit(1)
        username, password = sys.argv[1:]
        session = login(username, password)
        dump_cookies(session.cookies.get_dict(), 'cookies.json')

    worker = Worker(session)
    while True:
        try:
            title = worker.keep_online()
        except NotLoggedIn:
            print('**********Credentials expired, restart!**********')
            sys.exit(1)
        if title:
            print(time.ctime() + ' Accessed: ' + title)
            sleep_interval = random.gauss(50, 15)
            if sleep_interval < 3:
                sleep_interval = 3
            print('Sleep {}s'.format(round(sleep_interval, 2)))
            time.sleep(sleep_interval)
        else:
            print(time.ctime() + ' No posts under this forum, retry')
