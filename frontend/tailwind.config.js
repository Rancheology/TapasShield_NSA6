/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        industrial: {
          bg: "#090D16",
          panel: "#111827",
          border: "#1F2937",
          muted: "#374151",
          highlight: "#1E293B",
        },
        neon: {
          emerald: "#10B981",
          cyan: "#06B6D4",
          amber: "#F59E0B",
          crimson: "#EF4444",
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'Menlo', 'Consolas', 'Courier New', 'monospace'],
      }
    },
  },
  plugins: [],
}

