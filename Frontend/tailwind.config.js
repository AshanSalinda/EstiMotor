/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
        extend: {
            fontFamily: {
                sans: ["Inter", "sans-serif"],
            },
            colors: {
                dark: {
                    100: "#827E7E",
                    200: "#666666",
                    300: "#2B2B2B",
                    400: "#1B1B1B",
                    500: "#171717",
                    600: "#151515",
                    700: "#080808",
                },
                primary: {
                    100: "#F1F6F9",
                    200: "#D9EAF3",
                    300: "#B3D4E7",
                    400: "#4D9FDC",
                    500: "#0077CC",
                    600: "#0065A2",
                    700: "#004669",
                    800: "#003555",
                    900: "#002641",
                },
            },
            animation: {
                "shrink-fade": "shrink-and-fade 0.1s ease-in-out forwards",
                "grow-fade": "grow-and-fade 0.5s ease-in-out forwards",
            },
            keyframes: {
                "shrink-and-fade": {
                    "0%": { opacity: "1", height: "auto" },
                    "100%": { opacity: "0", height: "0" },
                },
                "grow-and-fade": {
                    "0%": { opacity: "0", height: "0" },
                    "100%": { opacity: "1", height: "auto" },
                },
            },
        },
    },
    plugins: [],
};
