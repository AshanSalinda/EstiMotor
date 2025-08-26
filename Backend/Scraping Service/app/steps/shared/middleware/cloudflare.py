import cloudscraper
from scrapy.http import HtmlResponse

from app.data.site_data import cloudflare_protected


class CloudflareBypassMiddleware:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def process_request(self, request, spider):
        # only handle the site that blocks by cloudflare bot protection
        if any(request.url.startswith(site) for site in cloudflare_protected):
            try:
                resp = self.scraper.get(request.url, timeout=30)
                return HtmlResponse(
                    url=request.url,
                    body=resp.content,
                    encoding="utf-8",
                    request=request,
                    status=resp.status_code
                )
            except Exception as e:
                spider.logger.error(f"Cloudflare bypass failed: {e}")
                return None
        return None
