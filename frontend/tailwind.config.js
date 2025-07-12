export default {
  content: [
    './public/index.html',
    './src/**/*.{html,js,jsx,css}',
    '../ai_agent/backend_core/Templates/**/*.html',
    '../ai_agent/backend_core/Static/css/django-tailwind.css',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#FFD700', // Gold
          dark: '#B8860B',   // Dark gold
          light: '#FFF8DC',  // Light gold
          hover: '#FFC300',
        },
        background: '#18181b', // Black
        surface: '#23232b',    // Slightly lighter black
        accent: '#fff',        // White
        error: '#ef4444',
        warning: '#facc15',
        info: '#0ea5e9',
        success: '#22c55e',
        royal: '#1a1a2e',      // Royal blue-black
        royalGold: '#FFD700',  // Royal gold
      },
      fontFamily: {
        display: ['Poppins', 'ui-sans-serif', 'system-ui'],
        body: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};