<template>
  <div class="min-h-screen bg-zinc-950 p-4 pb-12 font-sans">

    <div class="mb-8 mt-2 flex justify-between items-end">
      <div>
        <h1 class="text-3xl font-black text-zinc-100 tracking-tight uppercase">Métricas</h1>
        <p class="text-zinc-400 font-medium mt-1 tracking-wide text-sm">{{ mesActual }}</p>
      </div>
      <button
        @click="router.push('/')"
        class="bg-zinc-800 hover:bg-zinc-700 active:bg-zinc-600 text-zinc-300 p-3.5 rounded-xl border border-zinc-700 transition-all"
        title="Volver al tablero"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
        </svg>
      </button>
    </div>

    <div v-if="cargando" class="flex flex-col items-center justify-center mt-20">
      <div class="animate-spin rounded-full h-10 w-10 border-b-4 border-amber-500 mb-4"></div>
      <p class="text-zinc-500 font-medium uppercase tracking-widest text-sm">Cargando métricas...</p>
    </div>

    <div v-else class="space-y-8">

      <!-- KPI cards -->
      <div class="grid grid-cols-2 gap-3">

        <div class="bg-zinc-900 border border-zinc-700 rounded-xl p-5">
          <p class="text-zinc-500 text-xs font-bold uppercase tracking-widest mb-2">Motos activas</p>
          <p class="text-4xl font-black text-amber-500 font-mono">{{ datos.motos_activas }}</p>
          <p class="text-zinc-600 text-xs mt-1">en taller o listas</p>
        </div>

        <div class="bg-zinc-900 border border-zinc-700 rounded-xl p-5">
          <p class="text-zinc-500 text-xs font-bold uppercase tracking-widest mb-2">Facturado</p>
          <p class="text-4xl font-black text-emerald-400 font-mono">${{ formatearMonto(datos.facturado_mes) }}</p>
          <p class="text-zinc-600 text-xs mt-1">entregas este mes</p>
        </div>

        <div class="bg-zinc-900 border border-zinc-700 rounded-xl p-5">
          <p class="text-zinc-500 text-xs font-bold uppercase tracking-widest mb-2">Ingresos</p>
          <p class="text-4xl font-black text-sky-400 font-mono">{{ datos.ingresos_mes }}</p>
          <p class="text-zinc-600 text-xs mt-1">órdenes este mes</p>
        </div>

        <div
          class="rounded-xl p-5 border"
          :class="datos.ordenes_estancadas > 0
            ? 'bg-red-950/40 border-red-800/50'
            : 'bg-zinc-900 border-zinc-700'"
        >
          <p class="text-zinc-500 text-xs font-bold uppercase tracking-widest mb-2">Estancadas</p>
          <p
            class="text-4xl font-black font-mono"
            :class="datos.ordenes_estancadas > 0 ? 'text-red-400' : 'text-zinc-400'"
          >{{ datos.ordenes_estancadas }}</p>
          <p class="text-zinc-600 text-xs mt-1">+{{ datos.dias_umbral }} días sin avanzar</p>
        </div>

      </div>

      <!-- Detalle de órdenes estancadas -->
      <section v-if="datos.detalle_estancadas && datos.detalle_estancadas.length > 0">
        <div class="flex items-center gap-3 mb-4 border-b border-zinc-800 pb-3">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-red-400">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
          </svg>
          <h2 class="text-sm font-bold text-zinc-300 uppercase tracking-widest">Requieren atención</h2>
        </div>

        <div class="space-y-3">
          <div
            v-for="orden in datos.detalle_estancadas"
            :key="orden.id"
            @click="router.push(`/muro/${orden.id}`)"
            class="bg-zinc-900 border border-red-800/40 rounded-xl p-4 cursor-pointer hover:border-red-600 transition-all relative overflow-hidden"
          >
            <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-red-500"></div>
            <div class="flex justify-between items-center pl-2">
              <div>
                <p class="text-xl font-mono font-black text-zinc-100">{{ orden.placa }}</p>
                <p class="text-zinc-400 text-xs uppercase tracking-wide mt-0.5">{{ orden.modelo }}</p>
                <p class="text-zinc-500 text-xs mt-1">{{ orden.cliente }}</p>
              </div>
              <div class="text-right">
                <span class="text-red-400 font-black text-2xl font-mono">{{ orden.dias }}</span>
                <p class="text-red-600 text-xs font-bold uppercase">días</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div
        v-else-if="datos.detalle_estancadas"
        class="text-center py-10 bg-zinc-900 rounded-xl border border-dashed border-zinc-700"
      >
        <p class="text-emerald-500 font-bold text-sm uppercase tracking-widest">Todo al día</p>
        <p class="text-zinc-600 text-xs mt-1">Sin órdenes estancadas</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const cargando = ref(true);
const datos = ref({});

const mesActual = computed(() => {
  return new Date().toLocaleDateString('es-EC', { month: 'long', year: 'numeric' }).toUpperCase();
});

const formatearMonto = (valor) => {
  if (!valor && valor !== 0) return '—';
  return Number(valor).toLocaleString('es-EC', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

const cargarMetricas = async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/metricas/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
    });
    if (res.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      router.push('/login');
      return;
    }
    if (res.ok) datos.value = await res.json();
  } catch (e) {
    console.error('Error al cargar métricas:', e);
  } finally {
    cargando.value = false;
  }
};

onMounted(cargarMetricas);
</script>
