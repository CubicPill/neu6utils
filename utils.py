import json
import os
import sys

import requests
from bs4 import BeautifulSoup


def request_patch(slf, *args, **kwargs):
    timeout = kwargs.pop('timeout', 10)
    return slf.request_orig(*args, **kwargs, timeout=timeout)


setattr(requests.sessions.Session, 'request_orig', requests.sessions.Session.request)
requests.sessions.Session.request = request_patch


class NotLoggedIn(Exception): pass


class LoginException(Exception): pass


def try_login():
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
                os.remove('cookies.json')
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
    return session


def login(username, password):
    url = 'http://bt.neu6.edu.cn'
    session = requests.session()
    response = session.get(url)
    if response.status_code != 200:
        raise LoginException('Server returned code {}'.format(response.status_code))
    soup = BeautifulSoup(response.content, 'html5lib')
    form_data = dict()
    form_element = soup.find('form', {'name': 'login'})
    for element in form_element.find_all('input'):
        if element.has_attr('name'):
            value = ''
            if element.has_attr('value'):
                value = element['value']
            form_data[element['name']] = value
    form_data['username'] = username
    form_data['password'] = password
    response = session.post(url + '/' + form_element['action'], data=form_data)
    if response.status_code == 200:
        return session
    raise LoginException('Login failed')


def test_session(session: requests.session()):
    response = session.get('http://bt.neu6.edu.cn/home.php?mod=spacecp', allow_redirects=False)
    if response.status_code >= 500:
        raise LoginException('Server returned status code {}'.format(response.status_code))
    if response.status_code != 200:
        return False
    return True


def dump_cookies(cookies, path):
    with open(path, 'w') as f:
        json.dump(cookies, f)


def load_cookies(path) -> dict:
    with open(path) as f:
        return json.load(f)
