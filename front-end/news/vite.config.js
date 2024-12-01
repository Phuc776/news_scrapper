import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: "/",
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://database_api_service:8002', // Đảm bảo proxy yêu cầu đến đúng backend
    },
  },
})
