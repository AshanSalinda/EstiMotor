import time, random
from datetime import datetime

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from app.utils.logger import info


class Retry429Middleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        """
        Custom retry logic for handling HTTP 429 (Too Many Requests).

        - Uses exponential backoff starting at 60s (60, 120, 240...).
        - Adds a small random jitter (0–5s) to avoid synchronized retry bursts.
        - Blocks with time.sleep() before retrying the request.
        """

        if response.status == 429:
            print("Paused at:", datetime.now())

            # Track how many times this request has been retried
            retry_times = request.meta.get('retry_times', 0) + 1

            # Exponential backoff delay (60s, 120s, 240s, etc.)
            delay = 60 * (2 ** (retry_times - 1))

            # Add jitter to spread retries and avoid hammering the server
            delay += random.uniform(0, 5)
            # delay += random.random() * 5

            # Log pause & block execution for the delay duration
            info(f"[429] Pausing spider {spider.name} for {delay:.1f}s")
            time.sleep(delay)
            info(f"[429] Resuming spider {spider.name}")

            # Retry the request after the backoff delay
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        # For non-429 responses, fall back to default RetryMiddleware behavior
        return super().process_response(request, response, spider)
