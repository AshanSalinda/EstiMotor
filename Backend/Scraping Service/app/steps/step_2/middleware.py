from scrapy import signals
from datetime import datetime
from twisted.internet import reactor
from app.utils.message_queue import MessageQueue
from app.utils.logger import info


class RequestStats:
    _start_time = None
    _running_spiders_count = 0
    _total_links = 0
    _request_count = 0
    _response_count = 0
    _success_count = 0
    _failed_requests = []
    _scheduled_job_started = False 
    

    def __init__(self):
        RequestStats._running_spiders_count += 1
        if not RequestStats._start_time:
            RequestStats._start_time = datetime.now()


    @classmethod
    def from_crawler(cls, crawler):
        """This method is used by Scrapy to create spiders."""
        middleware = cls()

        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)

        if not RequestStats._scheduled_job_started:
            RequestStats._scheduled_job_started = True
            reactor.callLater(1, middleware.scheduled_task, crawler)

        return middleware
    

    def scheduled_task(self, crawler):
        """This function runs every 2 seconds."""
        if RequestStats._scheduled_job_started:            
            stats = self.calculate_stats()
            
            MessageQueue.enqueue({'stats': {
                'Status': 'Running',
                **stats,
                'Failure count': len(RequestStats._failed_requests),
            }})

            reactor.callLater(1, self.scheduled_task, crawler)
            
            
    def calculate_stats(self):
        """Calculate the total time taken and success rate."""

        # Avoid errors if start time is None
        if not RequestStats._start_time:
            return None 

        current_time = datetime.now()
        time_taken = str(current_time - RequestStats._start_time).split('.')[0]

        try:
            success_rate = str(int((RequestStats._success_count * 100) / RequestStats._request_count)) + '%'
        except ZeroDivisionError:
            success_rate = '0%'

        return {
            'Time Taken': time_taken,
            'Success Rate': success_rate,
            'Request Count': RequestStats._request_count,
            'Success Count': RequestStats._success_count
        }

    
    def spider_opened(self, spider):
        """Called when the spider is opened."""
        RequestStats._total_links += len(spider.start_urls)

    
    
    def spider_closed(self, spider, reason):
        info(f"Spider {spider.name} closed. Reason: {reason}")

        RequestStats._running_spiders_count -= 1
                        
        if RequestStats._running_spiders_count == 0:
            stats = self.calculate_stats()
            try:
                percentage = round((RequestStats._response_count * 100) / RequestStats._total_links, 2)
            except ZeroDivisionError:
                percentage = 100

            spider.storage.add_stat({
                **stats,
                'Failed Requests': RequestStats._failed_requests,
            })
            
            MessageQueue.enqueue({
                'stats': {
                    'Status': 'Completed',
                    **stats,
                    'Failure count': len(RequestStats._failed_requests),
                },
                'control': 'completed',
                'progress': percentage
            })
            
            
            RequestStats._scheduled_job_started = False
            RequestStats._start_time = None
            RequestStats._running_spiders_count = 0
            RequestStats._total_links = 0
            RequestStats._request_count = 0
            RequestStats._response_count = 0
            RequestStats._success_count = 0
            RequestStats._failed_requests = []
            

    def process_request(self, request, spider):
        """This is called for every request sent"""
        RequestStats._request_count += 1
        return None


    def process_response(self, request, response, spider):
        """This is called when responded"""
        if 200 <= response.status < 300:
            RequestStats._success_count += 1
            print(f"{request.meta.get('index')}\t{request.url}")
        else:
            index = request.meta.get('index')
            url = request.url
            err(f"{index}\t{url}")
            RequestStats._failed_requests.append({
                'index': index,
                'url': url,
                'error': response.status
            })
            
        RequestStats._response_count += 1
        try:
            percentage = round((RequestStats._response_count * 100) / RequestStats._total_links, 2)
            MessageQueue.enqueue({'progress': percentage, 'log': response.url})
        except Exception:
            pass

        return response


    def process_exception(self, request, exception, spider):
        """This is called when an exception is raised during request processing"""

        index = request.meta.get('index')
        url = request.url
        err(f"{index}\t{url}")
        RequestStats._failed_requests.append({
            'index': index,
            'url': url,
            'error': type(exception).__name__
        })
        
        RequestStats._response_count += 1
        MessageQueue.enqueue({'log': request.url})
        return None
