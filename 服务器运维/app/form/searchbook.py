import requests

isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
keword_url = 'http://t.yushu/im/v2/book/search?q={}&count={}&start={}'
from flask import current_app


def get(url, return_JSON=True):
    # 存储查询数据库
    r = requests.get(url)
    if r.status_code != 200:
        return {} if return_JSON else ''
    return r.json() if return_JSON else r.text


def search_by_isbn(isbn):
    url = isbn_url.format(isbn)
    result = get(url)
    return result


def search_by_keyword(keyword, page=1):
    url = keword_url.format(keyword, current_app.config['PAGE'], (page - 1) * current_app.config['PAGE'])
    print(app.config['PAGE'])
    result = get(url)
    return result
