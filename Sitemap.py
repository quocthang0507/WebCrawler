import os

from termcolor import cprint
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver

trang_chu = 'https://lamdong.gov.vn/SitePages/Home.aspx'
trang_con = ['https://lamdong.gov.vn/HOME/news/hotnews/SitePages/Home.aspx',
             'https://lamdong.gov.vn/HOME/news/chuyen-doi-so/SitePages/Home.aspx',
             'https://lamdong.gov.vn/HOME/news/tintrongnuoc/SitePages/Home.aspx',
             'https://lamdong.gov.vn/HOME/news/tin-quoc-te/SitePages/Home.aspx',
             'https://lamdong.gov.vn/HOME/news/tin-trong-tinh/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/dbnd/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/vpubnd/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/snv/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/stc/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/sgtvt/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/thanhtra/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/skhcn/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/sct/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/syt/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/stttt/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/stnmt/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/sldtbxh/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/stp/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/bandantoc/SitePages/Home.aspx',
             'https://lamdong.gov.vn/sites/liza/SitePages/Home.aspx']

max = 1500

# get domain name
main_domain = urlparse(trang_chu).netloc

# open browser
browser = webdriver.Edge(executable_path=os.path.join(
    os.getcwd(), 'webdrivers', 'msedgedriver.exe'))

browser.set_page_load_timeout(60)


def print_red(x: str): return cprint(x, 'red')


def get_urls_in_webpage(url: str, urls=[]):
    # wait for load fully webpage
    try:
        browser.get(url)
    except:
        return

    # page_source into beautiful_soup
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # get all <a href="..."> in current webpage
    for link in soup.find_all('a'):
        url = link.get('href')
        domain = urlparse(url).netloc
        if url not in urls and main_domain == domain and '/video/' not in url and 'Authenticate.aspx' not in url:
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
get_urls_in_webpage(trang_chu, urls)
if len(urls) < max:
    for url in trang_con:
        get_urls_in_webpage(url, urls)
        if len(urls) == max:
            break

export_to_file(urls)

browser.close()
