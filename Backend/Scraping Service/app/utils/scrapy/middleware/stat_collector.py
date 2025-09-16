from scrapy import signals
from app.utils.logger import info, err


class StatCollectorMiddleware:
    """Middleware to track request statistics."""
    @classmethod
    def from_crawler(cls, crawler):
        """This method is used by Scrapy to create spiders."""
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    @staticmethod
    def spider_closed(spider, reason):
        info(f"Spider {spider.name} closed. Reason: {reason}")

    @staticmethod
    def process_request(request, spider):
        """This is called for every request sent"""
        if not request.meta.get('redirect_times'):
            spider.progress_manager.add_request()
        return None

    @staticmethod
    def process_response(request, response, spider):
        """This is called when responded"""
        if 200 <= response.status < 300:
            spider.progress_manager.add_response(request.url)
            print(f"{request.meta.get('index')}\t{request.url}")
        else:
            index = request.meta.get('index')
            url = request.url
            err(f"{index}\t{response.status}\t{url}")
            spider.progress_manager.add_response(request.url, {
                'index': index,
                'url': url,
                'error': response.status
            })
        return response

    @staticmethod
    def process_exception(request, exception, spider):
        """This is called when an exception is raised during request processing"""
        index = request.meta.get('index')
        url = request.url
        error = type(exception).__name__
        err(f"{index}\t{error}\t{url}")
        spider.progress_manager.add_response(request.url, {
            'index': index,
            'url': url,
            'error': error
        })
        return None
