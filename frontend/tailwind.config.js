/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js}"] ,
  theme: {
    extend: {
      colors: {
        ink: "#0f172a",
        ember: "#f97316",
        tide: "#0ea5a4",
        moss: "#16a34a",
        fog: "#e2e8f0"
      }
    }
  },
  plugins: []
};
