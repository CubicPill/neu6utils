import random
import sys
import time

from bs4 import BeautifulSoup

from utils import login


class Worker:

    def __init__(self, username, password):
        self._session = login(username, password)

    def find_all_forums(self):
        url = 'http://bt.neu6.edu.cn/forum.php'
        response = self._session.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        forum_urls = [td.find('dt').find('a')['href'] for td in soup.find_all('td', {'class': 'fl_g'})]
        return ['http://bt.neu6.edu.cn/' + url for url in forum_urls][:-8]
        # get rid of the non-resource forums

    def random_access_post(self, form_url):
        response = self._session.get(form_url)
        soup = BeautifulSoup(response.content, 'html5lib')
        post_urls = ['http://bt.neu6.edu.cn/' + td.find('a', {'class': 's xst'})['href'] for td in
                     soup.find_all('th', {'class': 'new'})]
        response = self._session.get(random.choice(post_urls))
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup.find('title').text

    def keep_online(self):
        forums = self.find_all_forums()
        return self.random_access_post(random.choice(forums))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 ' + sys.argv[0] + ' <username> <password>')
        sys.exit(1)
    worker = Worker(sys.argv[1], sys.argv[2])
    while True:
        print(time.ctime() + ' Accessed: ' + worker.keep_online())
        time.sleep(random.randrange(10,120))
