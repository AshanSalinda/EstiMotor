settings = {
    "LOG_LEVEL": 'WARNING',
    "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
    "BOT_NAME": 'EstiMotor_scraper',
    "DOWNLOAD_FAIL_ON_DATALOSS": False,
    "DOWNLOADER_MIDDLEWARES": {
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        'app.steps.step_2.middleware.RequestStats': 543,
        'app.steps.shared.middleware.cloudflare.CloudflareBypassMiddleware': 560,
        'app.steps.shared.middleware.rate_limit.TooManyRequestsRetryMiddleware': 563
    }
}
