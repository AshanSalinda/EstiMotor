import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from "vite-plugin-pwa";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        react(),
        VitePWA({
            registerType: "autoUpdate",
            devOptions: {
                enabled: true,
            },
            manifest: {
                name: "EstiMotor",
                short_name: "EstiMotor",
                description: "Used Vehicle Price Prediction System",
                theme_color: "#000000",
                background_color: "#ffffff",
                display: "standalone",
                start_url: "/",
                icons: [
                    {
                        src: "/em192.png",
                        sizes: "192x192",
                        type: "image/png"
                    }
                ],
                screenshots: [
                    {
                        src: "/screenshot-1.png",
                        sizes: "1318x757",
                        type: "image/png",
                        form_factor: "wide"
                    },
                    {
                        src: "/screenshot-2.png",
                        sizes: "416x840",
                        type: "image/png",
                    },
                ],
            },
            includeAssets: [    // cache images
                "/em192.png",
                "/logo.svg",
                "/home-background.webp"
            ],
        }),
    ],
    server: {
        port: 3000,
    },
    preview: {
        port: 3000
    }
});