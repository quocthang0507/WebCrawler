import requests
import os

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver

url = 'https://lamdong.gov.vn/SitePages/Home.aspx'

main_domain = urlparse(url).netloc

browser = webdriver.Edge(executable_path=os.path.join(
    os.getcwd(), 'webdrivers', 'msedgedriver.exe'))

# wait for load fully webpage
browser.get(url)

soup = BeautifulSoup(browser.page_source, 'html.parser')

urls = []
max = 100

for link in soup.find_all('a'):
    url = link.get('href')
    domain = urlparse(url).netloc
    if url not in urls and main_domain == domain:
        if len(urls) <= max:
            urls.append(url)
            print(url)
        else:
            break

data_folder = os.path.join(os.getcwd(), 'data')
output_file = os.path.join(data_folder, 'urls.txt')
with open(output_file, mode='w', encoding='utf8') as writer:
    for url in urls:
        writer.write(f'{url}\n')

browser.close()
