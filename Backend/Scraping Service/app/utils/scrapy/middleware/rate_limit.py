import time
from twisted.internet import reactor, defer
from app.data.site_data import MAX_REQUESTS_PER_MINUTE

class RateLimitMiddleware:
    def __init__(self):
        self.last_request_time = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        """
        Enforces per-site request rate limiting.

        For each site defined in MAX_REQUESTS_PER_MINUTE,
        ensures we do not send requests faster than the
        configured requests-per-minute rate.
        """

        for site, limit in MAX_REQUESTS_PER_MINUTE.items():
            if request.url.startswith(site):
                last_time = self.last_request_time.get(site)

                if last_time:
                    # Time since last request to this site
                    elapsed = time.time() - last_time

                    # Minimum interval allowed between requests
                    min_interval = 60 / limit

                    # Delay required to maintain rate limit
                    delay = max(0, min_interval - elapsed)

                    # Enforce delay if requests are too fast
                    if delay > 0:
                        d = defer.Deferred()
                        reactor.callLater(delay, d.callback, None)
                        self.last_request_time[site] = time.time() + delay
                        return d  # Only this request is delayed

                # Update last request time for this site
                self.last_request_time[site] = time.time()

        return None
