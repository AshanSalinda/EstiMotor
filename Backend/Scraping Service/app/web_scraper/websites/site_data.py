patpat = {
    'url': 'https://www.patpat.lk/vehicle',
    'page_no': 722,
    'selectors': {
        'ads_link': 'div.result-img a',
        'next_button': 'ul.pagination li:last-child.disabled',
        'title': 'h2.item-title',
        'price': 'div.item-price p span:last-of-type',
        'rows': 'table.course-info tr',
    }
}

ikman = {
    'url': 'https://ikman.lk/en/ads/sri-lanka/cars',
    'page_no': 151,
    'selectors': {
        'ads_link': 'ul.list--3NxGO li a',
        'pagination': 'div.pagination--1bp3g nav',
        'title': 'h1.title--3s1R8',
        'price': 'div.amount--3NTpl',
        'table': 'div.ad-meta--17Bqm div.full-width--XovDn',
    }
}

riyasewana = {
    'url': 'https://riyasewana.com/search',
    'page_no': 1430,
    'selectors': {
        'ads_link': 'ul li.item.round h2 a',
        'next_button': 'div.pagination a:last-of-type',
        'title': '#content h1',
        'table': 'table.moret tbody',
    }
}