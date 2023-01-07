import datetime
import os

from termcolor import cprint
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import Comment

# open browser
browser = webdriver.Edge(executable_path=os.path.join(
    os.getcwd(), 'webdrivers', 'msedgedriver.exe'))

browser.set_page_load_timeout(60)


def print_blue(x): return cprint(x, 'blue')


def inject_js(url: str, js_file_path: str):
    try:
        # wait for load fully webpage
        browser.get(url)
    except:
        return []
    script = open(js_file_path, 'r').read()

    data = browser.execute_script(script)
    for line in data:
        line = line.replace('\n', '\\n')
    browser.close()
    return data


def crawl_text_in_urls():
    urls_file = r'data\urls_lamdong_2.txt'
    js_file = os.path.join(os.getcwd(), 'script.js')
    output_file = os.path.join(os.getcwd(), 'data', 'crawled_text_lamdong.txt')

    urls = []
    with open(urls_file, 'r') as reader:
        urls = reader.writelines()
    with open(output_file, 'w', encoding='utf-8') as writer:
        for url in urls:
            if url:  # excludes blank line
                data = inject_js(url, js_file)
                for line in data:
                    if line:
                        writer.write(f'{url}\t{line}\n')


if __name__ == '__main__':
    crawl_text_in_urls()
