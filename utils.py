import requests
from bs4 import BeautifulSoup


def login(username, password):
    url = 'http://bt.neu6.edu.cn'
    session = requests.session()
    response = session.get(url)

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
