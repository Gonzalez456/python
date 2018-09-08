import json
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
from requests import RequestException

def get_page_index(offset):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': '迪丽热巴图片',
        'armload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'gallery'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        Headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)'
        }
        request = requests.get(url, headers=Headers)
        if request.status_code == 200:
            return request.text
        return None
    except RequestException:
        print('请求出错')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        Headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)'
        }
        request = requests.get(url, headers=Headers)
        if request.status_code == 200:
            return request.text
        return None
    except RequestException:
        print('请求详情出错', url)
        return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)  #标题
    # print(html)json.decoder.JSONDecodeError: Extra data: line 1 column 3478 (char 3477)
    images_pattern = re.compile(r'var gallery =(.*?)var siblingList', re.S)
    result = re.search(images_pattern, html)
    print(result)
    if result:
        data = json.loads(result.group(1))
        if data in 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            return {
                'title' : title,
                'url' : url,
                'image' : images,

            }

def main():
    html = get_page_index(0)
    for url in parse_page_index(html):
        # print(url)
        html = get_page_detail(url)
        # print(html)
        if html:
            result = parse_page_detail(html,url)
            print(result)


if __name__ == '__main__':
    main()
