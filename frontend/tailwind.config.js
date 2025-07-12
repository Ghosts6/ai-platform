const plugin = require('tailwindcss/plugin');

module.exports = {
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
        'primary': '#00ADB5',
        'secondary': '#393E46',
        'background': '#222831',
        'surface': '#393E46',
        'accent': '#EEEEEE',
        'primary-hover': '#00c5cf',
        'secondary-hover': '#4a5058',
      },
      fontFamily: {
        display: ['Poppins', 'ui-sans-serif', 'system-ui'],
        body: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      keyframes: {
        typing: {
          '0%': { width: '0' },
          '100%': { width: '100%' },
        },
        blink: {
          '50%': { borderColor: 'transparent' },
        },
      },
      animation: {
        typing: 'typing 2s steps(20, end), blink .75s step-end infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    plugin(function({ addBase, theme }) {
      addBase({
        'body': {
          '&::-webkit-scrollbar': {
            width: '12px',
          },
          '&::-webkit-scrollbar-track': {
            background: theme('colors.surface'),
          },
          '&::-webkit-scrollbar-thumb': {
            backgroundColor: theme('colors.primary'),
            borderRadius: '20px',
            border: `3px solid ${'colors.surface'}`,
          },
        },
      });
    }),
  ],
};