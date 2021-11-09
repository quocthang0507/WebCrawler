from Sitemap_BaoChinhPhu import get_beautifulsoup_from_url

def get_text(url:str):
    soup = get_beautifulsoup_from_url(url)
    result