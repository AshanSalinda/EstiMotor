from scrapy import signals
from datetime import datetime, timezone
from app.api.websocket import enqueue_for_sending
from .web_scraper import pagination_ended_signal


class RequestStats:
    start_time = None
    running_spiders_count = 0
    total_links = 0
    response_count = 0
    request_count = 0
    success_responses = 0
    error_responses = []
    failed_requests = []

    def __init__(self):
        if not RequestStats.start_time:
            RequestStats.start_time = datetime.now(timezone.utc)
        RequestStats.running_spiders_count += 1
        print(RequestStats.start_time)
        print(RequestStats.running_spiders_count)
        print(RequestStats.total_links)
        print(RequestStats.response_count)
        print(RequestStats.request_count)
        print(RequestStats.success_responses)
        print(RequestStats.error_responses)
        print(RequestStats.failed_requests)
        # if RequestStats.start_time:
        #     RequestStats.start_time = datetime.now(timezone.utc)
        #     RequestStats.total_links = 0
        #     RequestStats.response_count = 0
        
        # self.request_count = 0
        # self.success_responses = 0
        # self.error_responses = []
        # self.failed_requests = []
        pass


    @classmethod
    def from_crawler(cls, crawler):
        """This method is used by Scrapy to create spiders."""
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(middleware.on_pagination_end, signal=pagination_ended_signal)
        return middleware
        
        
    def on_pagination_end(self, spider, data):
        ads_count = data.get('ads_count', 0)
        RequestStats.total_links += ads_count
    
    
    def spider_closed(self, spider):
        """Print stats when spider is closed"""
        RequestStats.running_spiders_count -= 1
        
        finish_time = datetime.now(timezone.utc)
        [time, ms] = str(finish_time - RequestStats.start_time).split('.')
        time_taken = f"{time}.{int(ms) // 1000}"
        
        success_rate = int((RequestStats.success_responses * 100) / RequestStats.request_count)
                
        if RequestStats.running_spiders_count == 0:
            spider.storage.add_stat("stats", {
                'Time Taken': time_taken,
                'Success Rate': success_rate,
                'Request Count': RequestStats.request_count,
                'Success Responses': RequestStats.success_responses,
                'Error Responses': RequestStats.error_responses,
                'Failed Requests': RequestStats.failed_requests,
            })
            print('All spiders closed')
            
            RequestStats.start_time = None
            RequestStats.running_spiders_count = 0
            RequestStats.total_links = 0
            RequestStats.response_count = 0
            RequestStats.request_count = 0
            RequestStats.success_responses = 0
            RequestStats.error_responses = []
            RequestStats.failed_requests = []


        # spider.storage.add_stat('Total Time Taken', time_taken)

        # spider.storage.add_stat(spider.name, {
        #     'Request Count': self.request_count,
        #     'Success Responses': self.success_responses,
        #     'Error Responses': self.error_responses,
        #     'Failed Requests': self.failed_requests,
        #     'Time Taken': time_taken
        # })
            


    def process_request(self, request, spider):
        """This is called for every request sent"""
        RequestStats.request_count += 1
        # enqueue_for_sending({'sent request': request.url})
        return None


    def process_response(self, request, response, spider):
        """This is called when responded"""
        if 200 <= response.status < 300:
            RequestStats.success_responses += 1
            # enqueue_for_sending({'success response': response.url})
        else:
            # enqueue_for_sending({'error response': response.url})
            RequestStats.error_responses.append({
                'index': request.meta.get('index'),
                'url': response.url,
                'error': response.status
            })
            
        is_ad = request.meta.get('index')
        if is_ad:
            RequestStats.response_count += 1
            try:
                percentage = round((RequestStats.response_count * 100) / RequestStats.total_links, 2)
                enqueue_for_sending({'progress': percentage})
                enqueue_for_sending({'log': response.url})
            except Exception as e:
                pass

        return response


    def process_exception(self, request, exception, spider):
        """This is called when an exception is raised during request processing"""
        RequestStats.failed_requests.append({
            'index': request.meta.get('index'),
            'url': request.url,
            'error': type(exception).__name__
        })
        
        RequestStats.response_count += 1
        enqueue_for_sending({'log': request.url})
        return None
