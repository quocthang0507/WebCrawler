import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from termcolor import cprint
from Sitemap_LamDong import export_to_file

url = {'url': 'https://baochinhphu.vn/', 'class': 'article-body'}

max = 10000


def print_red(x: str): return cprint(x, 'red')


def go_to_next_page(soup: BeautifulSoup):
    paging = soup.find("div", {"class": "paging"})
    for link in paging.find_all('a'):
        if link.get('class').contain('current'):
            next_page = link.findNext('a')
            return next_page.get('href')
    return None


def get_urls_in_webpage(url: str, urls=[], ext: str = '.vgp'):
    main_domain = urlparse(url).netloc

    request = requests.get(url)
    if request.ok:
        html = request.text
        soup = BeautifulSoup(html, 'html.parser')

        for link in soup.find_all('a'):
            url = link.get('href')
            domain = urlparse(url).netloc
            if url not in urls and main_domain == domain and url.endswith(ext):
                urls.append(url)
                get_urls_in_webpage(url, urls)
                if len(urls) == max:
                    break
        print_red(f'Đã lấy {len(urls)} URL')


urls = []
get_urls_in_webpage(url['url'], urls)
export_to_file(urls, 'urls_baochinhphu.txt')
