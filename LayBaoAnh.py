import requests
from bs4 import BeautifulSoup as bs


def get_source(url: str):
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    return None


def get_inline_text_in_tag(html_source: str):
    soup = bs(html_source, 'html.parser')
    trs = soup.find_all('tr')
    for row in trs:
        id = row.get('id').replace('sr-', '')
        text = row.find_all('td')[0].text
        yield (id, text)


if __name__ == '__main__':
    for year in range(2013, 2022):
        for month in range(1, 13):
            for str in {'Kho', 'so', 'sp', 'Kho0', 'so0', 'sp0'}:
                url = 'https://baoanhdantocmiennui.xembao.vn/Epaper/K_HO/{}/{}/files/data/search.html'.format(
                    year, f'{str}{month}')
                html = get_source(url)
                if html != None:
                    filename = fr'D:\OneDrive - dlu.edu.vn\CONGVIEC\TuDienKHoChuru\OCR\Text\So bao {month} nam {year}.txt'
                    data = get_inline_text_in_tag(html)
                    with open(filename, 'w+', encoding='utf-8') as f:
                        for row in data:
                            f.write(f'Trang số {row[0]}:\n\n')
                            f.write(f'{row[1]}\n\n')
                    print('Đã lấy xong tháng {} của năm {}'.format(month, year))
