import { createProxyMiddleware } from "http-proxy-middleware";


export function mlProxy(ML_SERVICE_URL) {
    return createProxyMiddleware({
        target: ML_SERVICE_URL,
        changeOrigin: true,
        logger: console,
        pathRewrite: () => '/predict'  // Always forward as '/predict'
    });
}
