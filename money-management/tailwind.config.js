/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  darkMode: 'media', 
  theme: {
    extend: {
      colors: {
        'light': {
          'primary': '#5D93BA',
          'secondary': '#91B8BD',
          'background': '#FBFDFE',
          'foreground': '#40514E',
          'accent': '#8850B8',
        },
        'dark': {
          'primary': '#0B3954',
          'secondary': '#435F67',
          'background': '#222831',
          'foreground': '#FAF9F9',
          'accent': '#D83F87',
        },
      },
    },
  },
  plugins: [],
}
