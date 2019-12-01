import requests
import urllib
import json
import os
from bs4 import BeautifulSoup

class Google:
    def __init__(self):
        self.GOOGLE_SEARCH_URL = 'https://www.google.co.jp/search'
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'})

    def search(self, keyword, maximum):
        print('Search :', keyword)
        result, total = [], 0
        query = self.generateQuery(keyword)
        while True:
            # 検索
            html = self.session.get(next(query)).text
            links = self.getLinks(html)

            # 検索結果の追加
            if not len(links):
                print('-> No more links')
                break
            elif len(links) > maximum - total:
                result += links[:maximum - total]
                break
            else:
                result += links
                total += len(links)

        print('-> Finally got', str(len(result)), 'links')
        return result

    def generateQuery(self, keyword):
        page = 0
        while True:
            params = urllib.parse.urlencode({
                    'q': keyword,
                    'tbm': 'isch',
                    'filter': '0',
                    'ijn': str(page)})

            yield self.GOOGLE_SEARCH_URL + '?' + params
            page += 1

    def getLinks(self, html):
        '''リンク取得'''
        soup = BeautifulSoup(html, 'lxml')
        elements = soup.select('.rg_meta.notranslate')
        jsons = [json.loads(e.get_text()) for e in elements]
        links = [js['ou'] for js in jsons]
        return links


def downloadImages(urls):
    for i, url in enumerate(urls):
        print("-> Downloading image", str(i + 1).zfill(4), end=" ")
        print(url)
        print(os.path.join(*["./googleImages", str(i + 1).zfill(4) + ".jpg"]))
        try:
            urllib.request.urlretrieve(
                url,
                os.path.join(*["./googleImages", str(i + 1).zfill(4) + ".jpg"]),
            )
            print("successful")
        except BaseException:
            print("failed")
            continue



google = Google()
# search images
results = google.search("顔", maximum=100)

downloadImages(results)

