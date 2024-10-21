/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        dark: {
          100: '#827E7E',
          200: '#666666',
          300: '#202020',
          400: '#171717',
          500: '#101010',
          600: '#080808'
        },
        primary: {
          100: '#F1F6F9',
          200: '#D9EAF3',
          300: '#B3D4E7',
          400: '#4D9FDC',
          500: '#0077CC',
          600: '#0065A2',
          700: '#004669',
          800: '#003555',
          900: '#002641',
        },
      }
    },
  },
  plugins: [],
};
