import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      devOptions: {
        enabled: true 
      },
      manifest: {
        name: 'TallerEC',
        short_name: 'TallerEC',
        description: 'Gestión inteligente para tu taller de motos',
        theme_color: '#09090b', 
        background_color: '#09090b', 
        display: 'standalone', 
        orientation: 'portrait', 
        icons: [
          {
            src: '/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any maskable'
          }
        ]
      }
    })
  ],
  // Configuración para el servidor de desarrollo (npm run dev)
  server: {
    host: '0.0.0.0', 
    port: 5173
  },
  // Configuración para el servidor de vista previa (npm run preview)
  preview: {
    host: '0.0.0.0',
    port: 4173
  }
})