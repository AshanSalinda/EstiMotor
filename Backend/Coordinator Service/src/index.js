import 'dotenv/config'
import express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";
import { createProxyMiddleware } from "http-proxy-middleware";
import { authMiddleware } from "./middleware/auth.js";
import { connectDB } from "./config/db.js";
import adminRoutes from "./routes/admin.js";


const PORT = process.env.PORT;
const SCRAPING_SERVICE_URL = process.env.SCRAPING_SERVICE_URL;


// Create Express app
const app = express();
app.use(express.json());
app.use(cookieParser());


app.use(cors({
    origin: process.env.FRONTEND_URL,
    credentials: true
}));


// -----------------------
// HTTP Proxy for Scraping Service
// -----------------------
const apiProxy = createProxyMiddleware({
    target: SCRAPING_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: { '^/scraping': '' },
    logger: console
})
app.use('/scraping', authMiddleware, apiProxy);


// -----------------------
// WebSocket Proxy
// -----------------------
const wsProxy = createProxyMiddleware({
    target: SCRAPING_SERVICE_URL.replace(/^http/, 'ws'),
    changeOrigin: true,
    pathRewrite: { '^/ws': '' },
    logger: console
});
app.use('/ws', authMiddleware, wsProxy);


// -----------------------
// General Express logger
// -----------------------
app.use((req, res, next) => {
    console.log(`[Express] ${req.method.padEnd(6)} ${req.url}`);
    next();
});


// -----------------------
// Native routes
// -----------------------
app.use("/admin", adminRoutes);


// -----------------------
// Start server
// -----------------------
const server = app.listen(PORT, async() => {
    await connectDB();
    console.log(`🚀 Coordinator Service running on port ${PORT}`);
});
// Attach WS upgrade handler
server.on('upgrade', wsProxy.upgrade);
