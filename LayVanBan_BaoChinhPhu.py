import os
import time

from Sitemap_BaoChinhPhu import get_beautifulsoup_from_url
from underthesea import sent_tokenize
from termcolor import cprint


def sentence_tokenize(text: str):
    sents = sent_tokenize(text)
    result = []
    for s in sents:
        s = s.strip()
        if s and not s.isdecimal():
            result.append(s)
    return result


def read_urls(filepath: str):
    with open(filepath, 'r', encoding='utf8') as reader:
        for line in reader:
            url = line.strip()
            if url:
                yield url


def get_text(url: str):
    start_time = time.time()

    soup = get_beautifulsoup_from_url(url)

    result = []
    if soup:
        divs = [soup.find("div", {"class": "article-body"}),
                soup.find("div", {"class": "article"}),
                soup.find("div", {"class": "main-article"})]
        for div in divs:
            if div:
                tags = [div.find_all('p'), div.find_all('div'),
                        div.find_all('td'), div.find_all('th')]
                for tag in tags:
                    for p in tag:
                        if p and p.get_text().strip():
                            sents = sentence_tokenize(p.get_text())
                            for s in sents:
                                result.append(s)
                end_time = time.time()
                print_blue(
                    f'Đã lấy văn bản trong {url}, trong {round(end_time - start_time, 2)} giây')
    else:
        end_time = time.time()
        print_red(
            f'Đã có lỗi khi truy cập trang web {url}, trong {round(end_time - start_time, 2)} giây')
    return result


def print_blue(x): return cprint(x, 'blue')


def print_red(x: str): return cprint(x, 'red')


if __name__ == '__main__':
    data_folder = os.path.join(os.getcwd(), 'data')
    urls_file = os.path.join(data_folder, 'urls_baochinhphu.txt')
    output_text_file = os.path.join(
        data_folder, 'crawled_sentences_baochinhphu.txt')

    with open(output_text_file, 'w', encoding='utf8') as writer:
        for url in read_urls(urls_file):
            sents = get_text(url)
            if len(sents) > 0:
                for s in sents:
                    s = s.strip()
                    if s:
                        writer.write(f'{s}\n')
            else:
                print_red(
                    f'Đã bỏ qua {url} vì không tìm thấy nội dung cần thu thập')
