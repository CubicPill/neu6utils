import time
from bs4 import BeautifulSoup
from utils import login
import sys


class Worker:

    def __init__(self, username, password):
        self._session = login(username, password)

    def find_all_forums(self):
        url='http://bt.neu6.edu.cn/forum.php'

    def random_access_post(self, form_url):
        pass

    def keep_online(self):
        pass


if __name__ == '__main__':
    worker = Worker(sys.argv[1], sys.argv[2])
    while True:
        worker.keep_online()
        time.sleep(300)
