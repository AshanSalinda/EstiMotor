import 'dotenv/config';
import express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";
import adminRoutes from "./routes/admin.js";
import userRoutes from "./routes/user.js";
import { connectDB } from "./config/db.js";
import { mlProxy } from "./proxies/mlProxy.js";
import { scrapingProxy } from "./proxies/scrapingProxy.js";
import { wsProxy } from "./proxies/wsProxy.js";
import { authMiddleware } from "./middleware/auth.js";

const PORT = process.env.PORT;
const SCRAPING_SERVICE_URL = process.env.SCRAPING_SERVICE_URL;
const ML_SERVICE_URL = process.env.ML_SERVICE_URL;

const app = express();
app.use(cookieParser());

app.use(cors({
    origin: process.env.FRONTEND_URL,
    credentials: true
}));

// -----------------------
// Proxies
// -----------------------
const ws = wsProxy(SCRAPING_SERVICE_URL);
app.use("/ws", ws);
app.use("/scraping", authMiddleware, scrapingProxy(SCRAPING_SERVICE_URL));
app.use("/predict", mlProxy(ML_SERVICE_URL));

// -----------------------
// Logger
// -----------------------
app.use((req, res, next) => {
    // Listen for the response to finish
    res.on("finish", () => {
        console.log(`[Express] ${req.method.padEnd(6)} ${req.originalUrl} [${res.statusCode}]`);
    });
    next();
});

// -----------------------
// Native routes (with JSON parser)
// -----------------------
app.use(express.json());
app.use("/api", userRoutes);
app.use("/admin", adminRoutes);

// -----------------------
// Start server
// -----------------------
const server = app.listen(PORT, async () => {
    await connectDB();
    console.log(`🚀 Coordinator Service running on port ${PORT}`);
});

// Attach WebSocket upgrade
server.on("upgrade", ws.upgrade);
