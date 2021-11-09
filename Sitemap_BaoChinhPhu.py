import requests
import os
import time

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
from termcolor import cprint

url = {'url': 'https://baochinhphu.vn/', 'class': 'article-body'}

max = 10000


def print_red(x: str): return cprint(x, 'red')


def print_blue(x): return cprint(x, 'blue')


def get_host_name(url: str):
    return "{0.scheme}://{0.netloc}/".format(urlsplit(url))


def get_next_page_from_url(url: str):
    host_name = get_host_name(url)
    soup = get_beautifulsoup_from_url(url)
    if soup:
        paging = soup.find("div", {"class": "paging"})
        if not paging:
            return None
        for link in paging.find_all('a'):
            if 'current' in link.get('class'):
                next_page = link.findNextSibling('a')
                if next_page:
                    next_url = next_page.get('href')
                    if host_name not in next_url:
                        next_url = urljoin(host_name, next_url)
                        return next_url
                else:
                    return None
    return None


def get_beautifulsoup_from_url(url: str):
    try:
        request = requests.get(url, timeout=60)
    except:
        return None
    if request.ok:
        html = request.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    return None


def get_urls_from_url(url: str, ext: str = '.vgp'):
    urls = []

    start_time = time.time()

    host_name = get_host_name(url)
    soup = get_beautifulsoup_from_url(url)

    if soup == None:
        end_time = time.time()
        print_red(
            f'Đã có lỗi khi truy cập địa chỉ {url} này, trong {round(end_time-start_time, 2)} giây')
        return []

    for link in soup.find_all('a'):
        url = link.get('href')
        if url and url.endswith(ext):
            if host_name not in url:
                url = urljoin(host_name, url)
            if url not in urls:
                urls.append(url)
    end_time = time.time()
    print_blue(
        f'Đã lấy được {len(urls)} URL, trong {round(end_time-start_time, 2)} giây')
    return urls


urls_in_home = get_urls_from_url(url['url'])
found_urls = []
data_folder = os.path.join(os.getcwd(), 'data')
output_urls_file = os.path.join(data_folder, 'urls_baochinhphu.txt')

with open(output_urls_file, mode='w', encoding='utf8') as writer:
    for url in urls_in_home:
        if url not in found_urls:
            found_urls.append(url)
            writer.write(f'{url}\n')
        while url:
            # Lấy các url nằm trên trang này
            urls = get_urls_from_url(url)
            for u in urls:
                if u not in found_urls:
                    found_urls.append(u)
                    writer.write(f'{u}\n')
            print_blue(f'Tổng cộng: {len(found_urls)}')
            # Di chuyển sang page tiếp theo (nếu có)
            url = get_next_page_from_url(url)
