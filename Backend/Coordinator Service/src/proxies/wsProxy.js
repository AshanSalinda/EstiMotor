import { createProxyMiddleware } from "http-proxy-middleware";


export function wsProxy(SCRAPING_SERVICE_URL) {
    return createProxyMiddleware({
        target: SCRAPING_SERVICE_URL.replace(/^http/, "ws"),
        changeOrigin: true,
        logger: console,
        pathRewrite: { "^/ws": "" },
        ws: true
    });
}
