import { createProxyMiddleware } from "http-proxy-middleware";


export function scrapingProxy(SCRAPING_SERVICE_URL) {
    return createProxyMiddleware({
        target: SCRAPING_SERVICE_URL,
        changeOrigin: true,
        logger: console,
        pathRewrite: { "^/scraping": "" }
    });
}
