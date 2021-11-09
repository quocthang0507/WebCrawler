import os
import datetime

from Sitemap_BaoChinhPhu import get_beautifulsoup_from_url
from underthesea import sent_tokenize
from string import punctuation
from termcolor import cprint


def sentence_tokenize(text: str):
    sents = sent_tokenize(text)
    result = []
    for s in sents:
        s = s.strip(punctuation)
        if not s.isdecimal():
            result.append(s)
    return result


def read_urls(filepath: str):
    with open(filepath, 'r', encoding='utf8') as reader:
        for line in reader:
            url = line.strip()
            if url:
                yield url


def get_text(url: str):
    soup = get_beautifulsoup_from_url(url)

    result = []
    if soup:
        div = soup.find("div", {"class": "article-body"})
        if div:
            for p in div.find_all('p'):
                if p and p.get_text().strip():
                    sents = sentence_tokenize(p.get_text())
                    for s in sents:
                        result.append(s)
    return result


def print_blue(x): return cprint(x, 'blue')


if __name__ == '__main__':
    data_folder = os.path.join(os.getcwd(), 'data')
    urls_file = os.path.join(data_folder, 'urls_baochinhphu.txt')
    output_text_file = os.path.join(
        data_folder, 'crawled_sentences_baochinhphu.txt')

    with open(output_text_file, 'w', encoding='utf8') as writer:
        for url in read_urls(urls_file):
            for t in get_text(url, get_full_text=False):
                writer.write(f'{t}\n')
            print_blue(
                f'Đã lấy xong trang web: {url} vào lúc {datetime.datetime.now()}')
