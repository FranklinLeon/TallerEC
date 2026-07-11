<template>
  <div class="min-h-screen bg-zinc-950 p-4 pb-12 font-sans">

    <div class="mb-6 mt-2 flex justify-between items-start">
      <div>
        <button @click="router.push('/')" class="text-zinc-400 hover:text-zinc-100 mb-2 flex items-center gap-1 text-sm font-bold transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          Volver al Tablero
        </button>
        <h1 class="text-3xl font-black text-zinc-100 tracking-tight uppercase">Archivo</h1>
        <p class="text-zinc-500 font-medium mt-1 tracking-wide text-sm">HISTORIAL DE TRABAJOS ENTREGADOS</p>
      </div>
    </div>

    <!-- Buscador -->
    <div class="mb-6">
      <div class="relative">
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-zinc-500">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
          </svg>
        </div>
        <input
          v-model="busqueda"
          type="text"
          class="bg-zinc-900 border-2 border-zinc-700 text-zinc-100 text-lg rounded-xl focus:ring-amber-500 focus:border-amber-500 block w-full pl-10 p-3 placeholder-zinc-500 uppercase font-mono"
          placeholder="Placa o nombre del cliente..."
        >
        <div v-if="buscando" class="absolute inset-y-0 right-0 flex items-center pr-3">
          <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-amber-500"></div>
        </div>
      </div>
    </div>

    <!-- Carga inicial -->
    <div v-if="cargando" class="flex flex-col items-center justify-center mt-20">
      <div class="animate-spin rounded-full h-10 w-10 border-b-4 border-zinc-500 mb-4"></div>
      <p class="text-zinc-500 font-medium uppercase tracking-widest text-sm">Cargando archivo...</p>
    </div>

    <div v-else class="space-y-3">

      <div v-if="ordenes.length === 0" class="text-center py-10 bg-zinc-900 rounded-xl border border-dashed border-zinc-700">
        <p class="text-zinc-500 text-sm">
          {{ busqueda ? 'Sin resultados para "' + busqueda + '"' : 'No hay trabajos archivados aún.' }}
        </p>
      </div>

      <div
        v-for="orden in ordenes"
        :key="orden.id"
        @click="router.push(`/muro/${orden.id}`)"
        class="bg-zinc-900 p-4 rounded-xl border border-zinc-800 cursor-pointer hover:border-zinc-500 active:bg-zinc-800 transition-all"
      >
        <div class="flex justify-between items-start gap-3">

          <!-- Izquierda: placa + modelo + cliente -->
          <div>
            <h3 class="text-xl font-mono font-bold text-zinc-200 tracking-tight">{{ orden.placa_moto || 'S/P' }}</h3>
            <p class="text-zinc-400 text-xs uppercase tracking-wide mt-0.5">{{ orden.modelo_moto }}</p>
            <p class="text-zinc-500 text-xs mt-1">{{ orden.nombre_cliente }}</p>
          </div>

          <!-- Derecha: fecha entrega + monto -->
          <div class="text-right shrink-0">
            <span class="text-emerald-400 font-black text-base font-mono">
              ${{ formatearMonto(orden.total_cobro) }}
            </span>
            <p class="text-zinc-600 text-[10px] mt-1">
              {{ orden.fecha_entrega ? formatearFecha(orden.fecha_entrega) : formatearFecha(orden.fecha_ingreso) }}
            </p>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const ordenes = ref([]);
const cargando = ref(true);
const buscando = ref(false);
const busqueda = ref('');

let debounceTimer = null;

const cargarHistorial = async (q = '') => {
  buscando.value = true;
  try {
    const params = q ? `?q=${encodeURIComponent(q)}` : '';
    const res = await fetch(`${import.meta.env.VITE_API_URL}/motos/historial/${params}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
    });
    if (res.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      router.push('/login');
      return;
    }
    if (res.ok) ordenes.value = await res.json();
  } catch (e) {
    console.error('Error al cargar historial:', e);
  } finally {
    buscando.value = false;
    cargando.value = false;
  }
};

watch(busqueda, (val) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => cargarHistorial(val.trim()), 350);
});

const formatearFecha = (fechaString) => {
  if (!fechaString) return '';
  return new Date(fechaString).toLocaleDateString('es-EC', { year: 'numeric', month: 'short', day: 'numeric' });
};

const formatearMonto = (valor) => {
  return Number(valor || 0).toLocaleString('es-EC', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

cargarHistorial();
</script>
