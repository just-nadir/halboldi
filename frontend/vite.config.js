import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true })
  ],
  define: { 'process.env': {} },

  // bu qator optimizeDeps muammolarining oldini oladi
  optimizeDeps: {
    include: ['vuetify'],
  },
})
