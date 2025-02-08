/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        dark: {
          primary: '#202123',    // Fundo principal
          secondary: '#2C2C2F',  // Fundo secundário
          accent: '#10A37F',     // Verde do ChatGPT
          border: '#3F3F46',     // Bordas
          text: {
            primary: '#FFFFFF',   // Texto principal
            secondary: '#A1A1AA', // Texto secundário
          }
        }
      }
    },
  },
  plugins: [],
};