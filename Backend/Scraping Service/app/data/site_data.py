patpat = {
    'name': 'patpat',
    'url': 'https://patpat.lk/en/sri-lanka/vehicle/all/toyota/land-cruiser-prado',
    'page_no': 7,
    # 'url': 'https://patpat.lk/en/sri-lanka/vehicle',
    # 'page_no': 1,
    'selectors': {
        'ads_link': 'section.container-hero > div:nth-last-child(2) > div > div:first-child > div > div:first-child > a',
        'next_button': 'section.container-hero > div:nth-last-child(2) > div:last-child > span:last-child.cursor-not-allowed',
        'title': 'section.left-div > section:first-child h2',
        'image': 'section.left-div > section:nth-child(2) img',
        'price': 'section.middle-div > div:first-child > div:first-child > span',
        'rows': 'section.detail-page-purple-gradient > div > div li',
    }
}

ikman = {
    'name': 'ikman',
    'url': 'https://ikman.lk/en/ads/sri-lanka/cars/toyota/land-cruiser-prado',
    'page_no': 12,
    # 'url': 'https://ikman.lk/en/ads/sri-lanka/vehicles',
    # 'page_no': 1,
    'selectors': {
        'ads_link': 'ul.list--3NxGO li a',
        'pagination': 'span.ads-count-text--1UYy_',
        'category': 'div.link-text--1Tj-x',
        'price': 'div.amount--3NTpl',
        'title': 'h1.title--3s1R8',
        'table': 'div.ad-meta--17Bqm div.full-width--XovDn',
    },
    'banned_categories': [
        'Auto Parts & Accessories',
        'Rentals',
        'Auto Services',
        'Bicycles',
        'Maintenance and Repair',
        'Boats & Water Transport',
    ]
}

riyasewana = {
    'name': 'riyasewana',
    'url': 'https://riyasewana.com/search/toyota/land-cruiser-prado',
    'page_no': 4,
    # 'url': 'https://riyasewana.com/search',
    # 'page_no': 1,
    'selectors': {
        'ads_link': 'ul .item h2 a',
        'next_button': 'div.pagination a:last-of-type',
        'current_button': 'div.pagination a.current',
        'category': ['a.vml:first-child', 'a.fm2:first-child'],
        'title': 'div#content > h1',
        'image': 'img#main-image',
        'table': ['table.moret tr', 'div#content > div.card-row']
    },
    'banned_categories': [
        'bicycles'
    ]
}

CLOUDFLARE_PROTECTED = [
    "https://riyasewana.com/"
]

MAX_REQUESTS_PER_MINUTE = {
    "https://riyasewana.com/": 100
}
