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


if __name__ == '__main__':
    output_file = os.path.join(os.getcwd(), 'data', 'sample_text_py.txt')
    js_file = os.path.join(os.getcwd(), 'script.js')
    data = inject_js(
        'https://demo4.dlu.edu.vn/gioi-thieu-khoa-cong-nghe-thong-tin/', js_file)
    with open(output_file, 'w', encoding='utf8') as writer:
        for line in data:
            writer.write(f"{line}\n")
