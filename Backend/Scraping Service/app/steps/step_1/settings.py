settings = {
    "LOG_LEVEL": 'WARNING',
    "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
    "BOT_NAME": 'EstiMotor_scraper',
    "DOWNLOAD_FAIL_ON_DATALOSS": False,
    "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    "DOWNLOADER_MIDDLEWARES": {
        'app.steps.step_1.middleware.RequestStats': 543,
    },
}
