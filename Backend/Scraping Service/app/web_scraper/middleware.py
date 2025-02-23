from scrapy import signals
from datetime import datetime, timezone
from twisted.internet import reactor
from app.utils.message_queue import MessageQueue
from app.utils.storage import Storage
from .web_scraper import pagination_ended_signal



class RequestStats:
    _start_time = None
    _running_spiders_count = 0
    _total_links = 0
    _request_count = 0
    _response_count = 0
    _success_count = 0
    _failed_requests = []
    _task_running = False 
    

    def __init__(self):
        RequestStats._running_spiders_count += 1
        if not RequestStats._start_time:
            RequestStats._start_time = datetime.now(timezone.utc)


    @classmethod
    def from_crawler(cls, crawler):
        """This method is used by Scrapy to create spiders."""
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(middleware.on_pagination_end, signal=pagination_ended_signal)
        if not RequestStats._task_running:
            RequestStats._task_running = True
            reactor.callLater(1, middleware.scheduled_task, crawler)
        return middleware
    
    def scheduled_task(self, crawler):
        """This function runs every 2 seconds."""
        if RequestStats._task_running:            
            stats = self.calculate_stats()
            
            MessageQueue.enqueue({'stats': {
                'Status': 'Running',
                **stats,
                'Failure count': len(RequestStats._failed_requests),
            }})

            reactor.callLater(1, self.scheduled_task, crawler)
            
            
    def calculate_stats(self):
        """Calculate the total time taken and success rate."""
        if not RequestStats._start_time:
            return None  # Avoid errors if start time is None

        current_time = datetime.now(timezone.utc)
        time_taken = str(current_time - RequestStats._start_time).split('.')[0]

        success_rate = str(int((RequestStats._success_count * 100) / RequestStats._request_count)) + '%'

        return {
            'Time Taken': time_taken,
            'Success Rate': success_rate,
            'Request Count': RequestStats._request_count,
            'Success Count': RequestStats._success_count
        }
        
        
    def on_pagination_end(self, spider, data):
        ads_count = data.get('ads_count', 0)
        RequestStats._total_links += ads_count
    
    
    def spider_closed(self, spider, reason):
        print(f"Spider {spider.name} closed. Reason: {reason}")

        RequestStats._running_spiders_count -= 1
                        
        if RequestStats._running_spiders_count == 0:
            RequestStats._task_running = False
            
            stats = self.calculate_stats()

            Storage.add_stat({
                **stats,
                'Failed Requests': RequestStats._failed_requests,
            })
            
            MessageQueue.enqueue({'stats': {
                'Status': 'Completed',
                **stats,
                'Failure count': len(RequestStats._failed_requests),
            }})
            
            MessageQueue.enqueue({'control': 'completed'})
            
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
        else:
            RequestStats._failed_requests.append({
                'index': request.meta.get('index'),
                'url': response.url,
                'error': response.status
            })
            
        is_ad = request.meta.get('index')
        if is_ad:
            RequestStats._response_count += 1
            try:
                percentage = round((RequestStats._response_count * 100) / RequestStats._total_links, 2)
                MessageQueue.enqueue({'progress': percentage})
                MessageQueue.enqueue({'log': response.url})
            except Exception:
                pass

        return response


    def process_exception(self, request, exception, spider):
        """This is called when an exception is raised during request processing"""
        RequestStats._failed_requests.append({
            'index': request.meta.get('index'),
            'url': request.url,
            'error': type(exception).__name__
        })
        
        RequestStats._response_count += 1
        MessageQueue.enqueue({'log': request.url})
        return None
