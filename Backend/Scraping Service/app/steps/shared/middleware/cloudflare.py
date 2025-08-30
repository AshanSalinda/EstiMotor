import cloudscraper
from scrapy.http import HtmlResponse

from app.data.site_data import CLOUDFLARE_PROTECTED


class CloudflareBypassMiddleware:
    def __init__(self):
        # Create a cloudscraper session (mimics a real browser)
        self.scraper = cloudscraper.create_scraper()

    def process_request(self, request, spider):
        """
        Intercepts requests to Cloudflare-protected sites.
        Uses cloudscraper to bypass bot protection and returns
        an HtmlResponse that Scrapy can process as if it came
        from the normal downloader.
        """

        # Only apply to sites listed as Cloudflare-protected
        if any(request.url.startswith(site) for site in CLOUDFLARE_PROTECTED):
            try:
                # Perform the request using cloudscraper
                resp = self.scraper.get(request.url, timeout=30)

                # Convert cloudscraper's response into a Scrapy-compatible HtmlResponse
                return HtmlResponse(
                    url=request.url,
                    body=resp.content,
                    encoding="utf-8",
                    request=request,
                    status=resp.status_code
                )
            except Exception as e:
                # Log and fall back to normal Scrapy downloader if bypass fails
                spider.logger.error(f"Cloudflare bypass failed: {e}")
                return None

        # For non-protected sites, let Scrapy handle as usual
        return None
