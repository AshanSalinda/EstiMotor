import time, random

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from app.utils.logger import info


class TooManyRequestsRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if response.status == 429:
            retry_times = request.meta.get('retry_times', 0) + 1

            delay = 60 * (2 ** (retry_times - 1))  # 1st retry = 60, 2nd = 120, 3rd = 240...
            delay += random.random() * 5  # small jitter (0s - 5s) to avoid bursts

            info(f"Sleeping spider {spider.name} for {delay:.1f}s due to Rate limit")
            time.sleep(delay)  # simple blocking delay
            info(f"Resuming spider {spider.name}")

            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        return super().process_response(request, response, spider)
