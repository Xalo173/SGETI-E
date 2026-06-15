/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0f172a',
        paper: '#f8fafc',
        accent: '#0f766e',
        warm: '#b45309',
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(15, 118, 110, 0.18), 0 24px 60px rgba(15, 23, 42, 0.18)',
      },
    },
  },
  plugins: [],
}
