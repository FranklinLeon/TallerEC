import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // <-- Importamos nuestro mapa

const app = createApp(App)
app.use(router) // <-- Le decimos a Vue que lo use
app.mount('#app')