import random
import sys
import time

from bs4 import BeautifulSoup

from utils import login

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 ' + sys.argv[0] + ' <username> <password>')
        sys.exit(1)
    username, password = sys.argv[1:]
    session = login(username, password)
