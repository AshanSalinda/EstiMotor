import random
from twisted.internet import reactor, defer
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from app.utils.logger import info


class Retry429Middleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        """
        Custom retry logic for handling HTTP 429 (Too Many Requests).

        - Uses exponential backoff starting at 60s (60, 120, 240...).
        - Adds a small random jitter (0–5s) to avoid synchronized retry bursts.
        - Uses Twisted Deferreds instead of time.sleep() so only this scraper waits.
        """

        if response.status == 429:
            # Track how many times this request has been retried
            retry_times = request.meta.get('retry_times', 0) + 1

            # Exponential backoff delay (60s, 120s, 240s, etc.)
            delay = 60 * (2 ** (retry_times - 1))

            # Add jitter to spread retries and avoid hammering the server
            delay += random.uniform(0, 5)

            info(f"[429] Pausing spider {spider.name} for {delay:.1f}s")

            # Retry after delay, without blocking other spiders
            d = defer.Deferred()

            def _do_retry():
                info(f"[429] Resuming spider {spider.name}")
                reason = response_status_message(response.status)
                result = self._retry(request, reason, spider) or response
                d.callback(result)

            reactor.callLater(delay, _do_retry)
            return d

        # For non-429 responses, fall back to default RetryMiddleware behavior
        return super().process_response(request, response, spider)
