import os
import datetime

from termcolor import cprint
from bs4 import BeautifulSoup
from selenium import webdriver
from underthesea import sent_tokenize
from string import punctuation


# open browser
browser = webdriver.Edge(executable_path=os.path.join(
    os.getcwd(), 'webdrivers', 'msedgedriver.exe'))

browser.set_page_load_timeout(60)


def print_blue(x): return cprint(x, 'blue')


def sentence_tokenize(text: str):
    sents = sent_tokenize(text)
    result = []
    for s in sents:
        s = s.strip(punctuation)
        if not s.isdecimal():
            result.append(s)
    return result


def get_text(url: str, get_full_text: bool = True):
    try:
        # wait for load fully webpage
        browser.get(url)
        # time.sleep(0.2)
    except:
        return []

    # page_source into beautiful_soup
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    result = []
    if not get_full_text:
        # get all <div class="contentPage"> or <div class="content_62b3f161"> in current webpage
        divs = soup.find_all("div", {"class": "contentPage"})
        if len(divs) == 0:
            divs = soup.find_all("div", {"class": "content_62b3f161"})
        for div in divs:
            for p in div.find_all('p'):
                if p and p.get_text().strip():
                    sents = sentence_tokenize(p.get_text())
                    for s in sents:
                        result.append(s)
    else:
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head',
            'input',
            'script',
            'style'
            # there may be more elements you don't want, such as "style", etc.
        ]
        text = soup.find_all(text=True)
        # print(set([t.parent.name for t in text]))
        for t in text:
            if t.parent.name not in blacklist and t.strip():
                result.append(t.strip())
    return result


def read_urls(filepath: str):
    with open(filepath, 'r', encoding='utf8') as reader:
        for line in reader:
            url = line.strip()
            if url:
                yield url


if __name__ == '__main__':
    data_folder = os.path.join(os.getcwd(), 'data')
    urls_file = os.path.join(data_folder, 'urls_lamdong.txt')
    output_text_file = os.path.join(data_folder, 'crawled_sentences_lamdong.txt')

    with open(output_text_file, 'w', encoding='utf8') as writer:
        for url in read_urls(urls_file):
            for t in get_text(url, get_full_text=False):
                writer.write(f'{t}\n')
            print_blue(
                f'Đã lấy xong trang web: {url} vào lúc {datetime.datetime.now()}')
