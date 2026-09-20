/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        college: {
          blue: '#1e3a8a',
          gold: '#fbbf24',
          dark: '#111827',
          gray: '#f3f4f6'
        }
      }
    },
  },
  plugins: [],
}
