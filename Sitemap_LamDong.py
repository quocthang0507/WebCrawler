import os
import time

from termcolor import cprint
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from LayVanBan_BaoChinhPhu import print_blue, print_red
from Sitemap_BaoChinhPhu import get_host_name

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

max = 999999

# get domain name
host_name = get_host_name(trang_chu)

# open browser
browser = webdriver.Edge(executable_path=os.path.join(
    os.getcwd(), 'webdrivers', 'msedgedriver.exe'))

browser.set_page_load_timeout(60)


def get_urls_from_url(url: str, urls=[], ext: str = '.aspx', sub_site='/sites/bandantoc'):
    # wait for load fully webpage
    start_time = time.time()
    try:
        browser.get(url)
    except:
        end_time = time.time()
        print_red(
            f'Đã có lỗi khi truy cập địa chỉ {url} này, trong {round(end_time - start_time, 2)} giây')
        return

    # page_source into beautiful_soup
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # get all <a href="..."> in current webpage
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith(ext):
            if not href.startswith(host_name) and href.startswith('/'):
                href = urljoin(host_name, href)
            if get_host_name(href) == host_name and href not in urls and '/video/' not in href and 'Authenticate.aspx' not in href:
                if sub_site and sub_site in href:
                    urls.append(href)
                else:
                    urls.append(href)
                    # if len(urls) == max:
                    #     break
    end_time = time.time()
    print_blue(
        f'Đã lấy thành công các URL trong {url} trong {round(end_time - start_time, 2)} giây')


def export_to_file(urls: list, file_name: str = 'urls_lamdong.txt'):
    data_folder = os.path.join(os.getcwd(), 'data')
    output_urls_file = os.path.join(data_folder, file_name)
    with open(output_urls_file, mode='w', encoding='utf8') as writer:
        for url in urls:
            writer.write(f'{url}\n')


def get_all_sub_site():
    found_urls = []
    file_name = 'urls_lamdong.txt'
    data_folder = os.path.join(os.getcwd(), 'data')
    output_urls_file = os.path.join(data_folder, file_name)
    with open(output_urls_file, mode='w', encoding='utf8') as writer:
        # Lay url trang chu
        get_urls_from_url(trang_chu, found_urls)
        # Lay url trang con
        for url in trang_con:
            get_urls_from_url(url, found_urls)
        # Lay tat ca url tren tung trang web
        for url in found_urls:
            urls = []
            writer.write(f'{url}\n')
            get_urls_from_url(url, urls)

            len0 = len(found_urls)
            for u in urls:
                if u not in found_urls:
                    found_urls.append(u)
                    writer.write(f'{u}\n')
            len1 = len(found_urls)
            if len1 > len0:
                print_blue(f'Đã lấy thêm {len1 - len0} urls')
        # Lay them mot lan nua
        for url in found_urls:
            urls = []
            writer.write(f'{url}\n')
            get_urls_from_url(url, urls)

            len0 = len(found_urls)
            for u in urls:
                if u not in found_urls:
                    found_urls.append(u)
                    writer.write(f'{u}\n')
            len1 = len(found_urls)
            if len1 > len0:
                print_blue(f'Đã lấy thêm {len1 - len0} urls')

    # export_to_file(urls)

    browser.close()


def get_bandantoc_site():
    found_urls = []
    file_name = 'urls_lamdong_bandantoc.txt'
    data_folder = os.path.join(os.getcwd(), 'data')
    output_urls_file = os.path.join(data_folder, file_name)
    with open(output_urls_file, mode='w', encoding='utf8') as writer:
        get_urls_from_url(
            'https://lamdong.gov.vn/sites/bandantoc/SitePages/Home.aspx', found_urls)
        # Lay tat ca url tren tung trang web
        for url in found_urls:
            urls = []
            writer.write(f'{url}\n')
            get_urls_from_url(url, urls)

            len0 = len(found_urls)
            for u in urls:
                if u not in found_urls:
                    found_urls.append(u)
                    writer.write(f'{u}\n')
            len1 = len(found_urls)
            if len1 > len0:
                print_blue(f'Đã lấy thêm {len1 - len0} urls')
        # Lay them mot lan nua
        for url in found_urls:
            urls = []
            writer.write(f'{url}\n')
            get_urls_from_url(url, urls)

            len0 = len(found_urls)
            for u in urls:
                if u not in found_urls:
                    found_urls.append(u)
                    writer.write(f'{u}\n')
            len1 = len(found_urls)
            if len1 > len0:
                print_blue(f'Đã lấy thêm {len1 - len0} urls')

    browser.close()
