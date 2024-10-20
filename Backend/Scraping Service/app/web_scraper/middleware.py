from scrapy import signals
from datetime import datetime, timezone
from app.api.websocket import enqueue_for_sending
from .web_scraper import pagination_ended


class RequestStats:
    start_time = datetime.now(timezone.utc)
    sent_requests = 0
    response_count = 0

    def __init__(self):
        self.start_time = None
        self.request_count = 0
        self.success_responses = 0
        self.error_responses = []
        self.failed_requests = []


    @classmethod
    def from_crawler(cls, crawler):
        """This method is used by Scrapy to create spiders."""
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(middleware.on_pagination_end, signal=pagination_ended)
        return middleware
        
        
    def on_pagination_end(self, spider, data):
        ads_count = data.get('ads_count', 0)
        print(spider.name, "pagination ended, ads count :", ads_count)
    
    
    def spider_closed(self, spider):
        """Print stats when spider is closed"""

        finish_time = datetime.now(timezone.utc)
        [time, ms] = str(finish_time - RequestStats.start_time).split('.')
        time_taken = f"{time}.{int(ms) // 1000}"

        spider.storage.add_stat('Total Time Taken', time_taken)

        spider.storage.add_stat(spider.name, {
            'Request Count': self.request_count,
            'Success Responses': self.success_responses,
            'Error Responses': self.error_responses,
            'Failed Requests': self.failed_requests,
            'Time Taken': time_taken
        })


    def process_request(self, request, spider):
        """This is called for every request sent"""
        RequestStats.sent_requests += 1
        self.request_count += 1
        enqueue_for_sending({'sent request': request.url})
        return None


    def process_response(self, request, response, spider):
        """This is called when responded"""
        if 200 <= response.status < 300:
            self.success_responses += 1
            enqueue_for_sending({'success response': response.url})
        else:
            enqueue_for_sending({'error response': response.url})
            self.error_responses.append({
                'index': request.meta.get('index'),
                'url': response.url,
                'status': response.status
            })

        RequestStats.response_count += 1
        percentage = (RequestStats.response_count * 100) / RequestStats.sent_requests
        # print(f"\r{percentage:.2f}% completed", end='')

        return response


    def process_exception(self, request, exception, spider):
        """This is called when an exception is raised during request processing"""
        self.failed_requests.append({
            'index': request.meta.get('index'),
            'url': request.url,
            'error': type(exception).__name__
        })
        
        enqueue_for_sending({'error response': request.url})
        return None
