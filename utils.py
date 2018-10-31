import json

import requests
from bs4 import BeautifulSoup


class NotLoggedIn(Exception): pass


class LoginException(Exception): pass


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
    raise Exception('Login failed')


def test_session(session: requests.session()):
    response = session.get('http://bt.neu6.edu.cn/home.php?mod=spacecp', allow_redirects=False)
    if response.status_code != 200:
        return False
    return True


def dump_cookies(cookies, path):
    with open(path, 'w') as f:
        json.dump(cookies, f)


def load_cookies(path) -> dict:
    with open(path) as f:
        return json.load(f)
