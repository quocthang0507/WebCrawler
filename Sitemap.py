import os
from termcolor import cprint

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver

url = 'https://lamdong.gov.vn/SitePages/Home.aspx'
max = 100
extended = True  # used for get more urls from existing url in urls

# get domain name
main_domain = urlparse(url).netloc

# open browser
browser = webdriver.Edge(executable_path=os.path.join(
    os.getcwd(), 'webdrivers', 'msedgedriver.exe'))


def print_red(x: str): return cprint(x, 'red')


def get_urls_in_webpage(url: str, urls=[]):
    # wait for load fully webpage
    browser.get(url)
    # page_source into beautiful_soup
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    # get all <a href="..."> in current webpage
    for link in soup.find_all('a'):
        url = link.get('href')
        domain = urlparse(url).netloc
        if url not in urls and main_domain == domain and '.aspx' in url and '/video/' not in url and 'Authenticate.aspx' not in url:
            urls.append(url)
            if len(urls) == max:
                break
    print_red(f'Đã lấy {len(urls)} URL')


def export_to_file(urls: list):
    data_folder = os.path.join(os.getcwd(), 'data')
    output_urls_file = os.path.join(data_folder, 'urls.txt')
    with open(output_urls_file, mode='w', encoding='utf8') as writer:
        for url in urls:
            writer.write(f'{url}\n')


urls = []
get_urls_in_webpage(url, urls)
if len(urls) < max:
    for url in urls:
        get_urls_in_webpage(url, urls)
        if len(urls) == max:
            break

export_to_file(urls)

browser.close()
