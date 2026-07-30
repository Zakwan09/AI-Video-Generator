/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: "#0a0908",
          900: "#121110",
          800: "#1c1a18",
          700: "#2a2622",
        },
        gold: {
          400: "#e8c473",
          500: "#d4af37",
          600: "#b8932c",
        },
      },
      fontFamily: {
        display: ["'Cormorant Garamond'", "serif"],
        body: ["'Inter'", "sans-serif"],
      },
    },
  },
  plugins: [],
};
