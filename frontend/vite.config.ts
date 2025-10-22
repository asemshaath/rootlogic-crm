import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: parseInt(process.env.PORT ?? '5173', 10),
    allowedHosts: ['*'],
    strictPort: true,
    hmr: {
      clientPort: 443, // ensure correct websocket port for HTTPS
    },
  },
  preview: {
    allowedHosts: ['*'],
  },
})
