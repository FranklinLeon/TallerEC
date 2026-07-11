import { createRouter, createWebHistory } from 'vue-router';

import TableroKanban from './components/TableroKanban.vue';
import RegistroCliente from './components/RegistroCliente.vue';
import MuroActividad from './components/MuroActividad.vue';
import SeguimientoCliente from './components/SeguimientoCliente.vue';
import HistorialMotos from './components/HistorialMotos.vue';
import LoginTaller from './components/LoginTaller.vue';
import DashboardMetricas from './components/DashboardMetricas.vue';

const routes = [
  { path: '/login', name: 'Login', component: LoginTaller },
  { path: '/', name: 'Tablero', component: TableroKanban, meta: { requiresAuth: true } },
  { path: '/registro', name: 'Registro', component: RegistroCliente, meta: { requiresAuth: true } },
  { path: '/historial', name: 'Historial', component: HistorialMotos, meta: { requiresAuth: true } },
  { path: '/muro/:id', name: 'Muro', component: MuroActividad, meta: { requiresAuth: true } },
  { path: '/metricas', name: 'Metricas', component: DashboardMetricas, meta: { requiresAuth: true } },
  
  // RUTA PÚBLICA (El cliente final no necesita token)
  { path: '/seguimiento/:hash', name: 'Seguimiento', component: SeguimientoCliente },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guardián de Rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  
  if (to.meta.requiresAuth && !token) {
    next('/login');
  } else {
    next();
  }
});

export default router;