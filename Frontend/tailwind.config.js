/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
        extend: {
            fontFamily: {
                sans: ["Inter", "sans-serif"],
            },
            keyframes: {
                gradientMove: {
                    '0%': { backgroundPosition: '0% 100%' },
                    '100%': { backgroundPosition: '0% 0%' }
                },
                fadeIn: {
                    '0%': { opacity: 0, transform: "scale(0.5)" },
                    '50%': { opacity: 0.5, transform: "scale(1)" },
                    '100%': { opacity: 1, transform: "scale(1)" }
                },
                glow: {
                    '0%': { textShadow: '5px 0 20px #1E90FF80, -5px 0 20px #1E90FF80, 0 -5px 20px #1E90FF80, 0 5px 20px #1E90FF80' },
                    '30%': { textShadow: '5px 0 35px #1E90FFC0, -5px 0 35px #1E90FFC0, 0 -5px 35px #1E90FFC0, 0 5px 35px #1E90FFC0' },
                    '100%': { textShadow: '1px 0 20px #1E90FF20, -1px 0 20px #1E90FF20, 0 -1px 20px #1E90FF20, 0 1px 20px #1E90FF20' },
                }
            },
            animation: {
                gradientMove: 'gradientMove 3s ease',
                fadeIn: 'fadeIn 0.8s ease',
                glow: 'glow 2s ease',
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
                    500: '#1E90FF',     // #3b82f6
                    600: '#2563eb',
                    700: '#1d4ed8',
                    800: '#1e40af',
                    900: '#1e3a8a',
                    950: '#172554',
                },
                custom:{
                    main: '#14B5FF'
                }
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
        }
    ],
};
