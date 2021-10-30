import os
import datetime

from termcolor import cprint
from bs4 import BeautifulSoup
from selenium import webdriver

# open browser
browser = webdriver.Edge(executable_path=os.path.join(
    os.getcwd(), 'webdrivers', 'msedgedriver.exe'))

browser.set_page_load_timeout(60)


def print_blue(x): return cprint(x, 'blue')


def get_text(url: str):
    try:
        # wait for load fully webpage
        browser.get(url)
    except:
        return []

    # page_source into beautiful_soup
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # get all <div class="contentPage"> or <div class="content_62b3f161"> in current webpage
    # divs = soup.find_all("div", {"class": "contentPage"})
    # if len(divs) == 0:
    #     divs = soup.find_all("div", {"class": "content_62b3f161"})
    result = []
    p_tags = soup.find('p')
    if p_tags != None and len(p_tags) > 0:
        for p in p_tags:
            text = p.text.strip()
            if text:
                result.append(text)
    return result


def read_urls(filepath: str):
    with open(filepath, 'r', encoding='utf8') as reader:
        for line in reader:
            url = line.strip()
            if url:
                yield url


data_folder = os.path.join(os.getcwd(), 'data')
urls_file = os.path.join(data_folder, 'urls.txt')
output_text_file = os.path.join(data_folder, 'crawled_text.txt')

with open(output_text_file, 'w', encoding='utf8') as writer:
    for url in read_urls(urls_file):
        for t in get_text(url):
            writer.write(f'{t}\n')
        print_blue(
            f'Đã lấy xong trang web: {url} vào lúc {datetime.datetime.now()}')
