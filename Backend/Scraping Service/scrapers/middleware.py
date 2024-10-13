from scrapy import signals

class RequestStatsMiddleware:
    def __init__(self):
        self.request_count = 0
        self.success_responses = 0
        self.error_responses = []
        self.failed_requests = []

    @classmethod
    def from_crawler(cls, crawler):
        """This method is used by Scrapy to create spiders."""
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware


    def spider_opened(self, spider):
        """Reset stats when spider is opened"""
        self.request_count = 0
        self.success_responses = 0
        self.error_responses = []
        self.failed_requests = []


    def spider_closed(self, spider):
        """Print stats when spider is closed"""
        spider.storage.add_stat({
            'Request Count': self.request_count,
            'Success Responses': self.success_responses,
            'Error Responses': self.error_responses,
            'Failed Requests': self.failed_requests,
        })


    def process_request(self, request, spider):
        """This is called for every request sent"""
        self.request_count += 1
        return None


    def process_response(self, request, response, spider):
        """This is called when responded"""
        if 200 <= response.status < 300:
            self.success_responses += 1
        else:
            self.error_responses.append({
                'index': request.meta.get('index'),
                'url': response.url,
                'status': response.status
            })

        return response


    def process_exception(self, request, exception, spider):
        """This is called when an exception is raised during request processing"""
        self.failed_requests.append({
            'index': request.meta.get('index'),
            'url': response.url,
            'error': type(exception).__name__
        })

        return None
