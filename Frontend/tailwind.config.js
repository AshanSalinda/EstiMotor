/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
        extend: {
            screens: {
                onlyMd: { min: "600px", max: "1023px" },
                md: { min: "600px"},
            },
            fontFamily: {
                sans: ["Inter", "sans-serif"],
                monoSpace: ["Azeret Mono", "Inter", "sans-serif"]
            },
            keyframes: {
                gradientMove: {
                    '0%': { backgroundPosition: '0% 100%' },
                    '100%': { backgroundPosition: '0% 0%' }
                },
                fadeIn: {
                    '0%': { opacity: 0, transform: "scale(0.9)" },
                    '40%': { opacity: 0.5, transform: "scale(1.05)" },
                    '100%': { opacity: 1, transform: "scale(1)" }
                },
                bounce: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                },
                glow: {
                    '0%': { textShadow: '5px 0 var(--glow-spade-0) var(--glowBlue), -5px 0 var(--glow-spade) var(--glowBlue), 0 -5px var(--glow-spade) var(--glowBlue), 0 5px var(--glow-spade) var(--glowBlue)' },
                    '30%': { textShadow: '12px 12px var(--glow-spade) var(--glowBlue-50), -12px 12px var(--glow-spade) var(--glowBlue-50), 12px -12px var(--glow-spade) var(--glowBlue-50), -12px -12px var(--glow-spade) var(--glowBlue-50)' },
                    '100%': { textShadow: '1px 0 20px var(--glowBlue), -1px 0 20px var(--glowBlue), 0 -1px 20px var(--glowBlue), 0 1px 20px var(--glowBlue)' },
                }
            },
            animation: {
                gradientMove: 'gradientMove 3.5s ease',
                fadeIn: 'fadeIn 1s ease',
                glow: 'glow 3.5s ease',
            },
            colors: {
                dark: {
                    100: "#827E7E",     // Header Title
                    200: "#666666",     // Stepper
                    300: "#2A2A2A",     // Header
                    400: "#202020",
                    500: "#1B1B1B",     // SideNavbar, DataPanel Header
                    600: "#171717",     
                    700: "#101010",     // background
                    800: "#080808",     // DataPanel background
                },
                primary: {
                    50: '#eff6ff',
                    100: '#dbeafe',
                    200: '#bfdbfe',
                    300: '#93c5fd',
                    400: '#60a5fa',
                    450: '#0ab7ff',
                    500: '#1E90FF',     // #3b82f6 #1E90FF
                    600: '#2563eb',
                    700: '#1d4ed8',
                    800: '#1e40af',
                    900: '#1e3a8a',
                    950: '#172554',
                },
                custom:{
                    main: '#14B5FF'
                },
                glowBlue: "#1E90FFF0",
            },
        }
    },
    plugins: [
        function ({ addUtilities }) {
            addUtilities({
                '.text-shadow': {
                    textShadow: '3px 3px 15px #000000, -3px 3px 15px #000000, 3px -3px 15px #000000, -3px -3px 15px #000000',
                },
                '.text-shadow-white': {
                    textShadow: '0 0 4px #FFFFFF, 0 0 4px #FFFFFF',
                },
            });
        },
        function ({ addBase }) {
            addBase({
                ":root": { // values glow animation
                    "--glowBlue": "#005ebb20",
                    "--glowBlue-50": "#005ebb",
                    "--glow-spade-0": "20px",
                    "--glow-spade": "20px",
                },
            });
        }
    ],
};
