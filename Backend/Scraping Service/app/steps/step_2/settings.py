settings = {
    "LOG_LEVEL": 'WARNING',
    "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
    "BOT_NAME": 'EstiMotor_scraper',
    "DOWNLOAD_FAIL_ON_DATALOSS": False,
    "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36',
    # "RANDOM_UA_TYPE": 'desktop.random',
    "DOWNLOADER_MIDDLEWARES": {
        # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        # 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        'app.steps.step_2.middleware.RequestStats': 543,
        'app.steps.shared.middleware.cloudflare.CloudflareBypassMiddleware': 560,
        'app.steps.shared.middleware.rate_limit.TooManyRequestsRetryMiddleware': 563
    }
}
