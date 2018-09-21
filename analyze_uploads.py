import sys

from bs4 import BeautifulSoup

from utils import login


def parse_page(content):
    soup = BeautifulSoup(content, 'html5lib')
    rows = soup.find('table', {'class': 'dt'}).find_all('tr')[1:]
    if not rows:
        return None
    result = list()
    for r in rows:
        _, title, up, _, _, t = r.find_all('td')
        if 'GB' not in up.text or '小时' not in t.text:
            continue
        result.append((title.text, float(up.text[:-3]) * 1024, float(t.text[:-2])))
    return result


URL = 'http://bt.neu6.edu.cn/home.php?mod=spacecp&ac=plugin&op=credit&id=torrent:traffics&page={page}'
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 ' + sys.argv[0] + ' <username> <password>')
        sys.exit(1)
    username, password = sys.argv[1:]

    session = login(username, password)

    page = 1
    results = list()
    while True:
        response = session.get(URL.format(page=page))
        ret = parse_page(response.content)
        if ret:
            results.extend(ret)
        else:
            break
        page += 1
    results.sort(key=lambda r: r[1] / r[2], reverse=True)
    with open('stats.csv', 'w', encoding='utf-8-sig') as f:
        f.write('"Title","Upload/MB","Time/h","Speed/(MB/h)"\n')
        for r in results:
            print('{}\t{}\t{}\t{}'.format(r[0], r[1], r[2], round(r[1] / r[2], 6)) + ' MB/h')
            f.write('"{}",{},{},{}\n'.format(r[0], r[1], r[2], round(r[1] / r[2], 6)))
