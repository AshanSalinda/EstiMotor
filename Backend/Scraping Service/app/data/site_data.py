patpat = {
    'name': 'patpat',
    # 'url': 'https://patpat.lk/en/sri-lanka/vehicle/all/toyota/land-cruiser-prado',
    # 'page_no': 8,
    'url': 'https://www.patpat.lk/vehicle',
    'page_no': 1,
    'selectors': {
        'ads_link': 'section.container-hero > div:nth-last-child(2) > div > div:first-child > div > div:first-child > a',
        'next_button': 'section.container-hero > div:nth-last-child(2) > div:last-child > span:last-child.cursor-not-allowed',
        'title': 'section.left-div > section:first-child > div > div:first-child > h2',
        'price': 'section.middle-div > div:first-child > div:first-child > span',
        'rows': 'section.detail-page-purple-gradient > div > div li',
    }
}

ikman = {
    'name': 'ikman',
    # 'url': 'https://ikman.lk/en/ads/sri-lanka/cars/toyota/land-cruiser-prado',
    # 'page_no': 11,
    'url': 'https://ikman.lk/en/ads/sri-lanka/cars',
    'page_no': 1,
    'selectors': {
        'ads_link': 'ul.list--3NxGO li a',
        'pagination': 'span.ads-count-text--1UYy_',
        'title': 'h1.title--3s1R8',
        'price': 'div.amount--3NTpl',
        'table': 'div.ad-meta--17Bqm div.full-width--XovDn',
    }
}

riyasewana = {
    'name': 'riyasewana',
    # 'url': 'https://riyasewana.com/search/toyota/land-cruiser-prado',
    # 'page_no': 1480,
    'url': 'https://riyasewana.com/search',
    'page_no': 1,
    'selectors': {
        'ads_link': 'ul .item h2 a',
        'next_button': 'div.pagination a:last-of-type',
        'current_button': 'div.pagination a.current',
        'title': '#content h1',
        'table': ['table.moret tr', '#content > div.card-row']
    }
}

CLOUDFLARE_PROTECTED = [
    "https://riyasewana.com/"
]

MAX_REQUESTS_PER_MINUTE = {
    "https://riyasewana.com/": 100
}
