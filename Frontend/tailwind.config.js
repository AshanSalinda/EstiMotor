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
                    '100%': { backgroundPosition: '0% 0%' },
                },
            },
            animation: {
                gradientMove: 'gradientMove 3s ease',
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
            });
        }
    ],
};
