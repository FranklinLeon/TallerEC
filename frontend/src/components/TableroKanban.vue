<template>
  <div class="min-h-screen bg-zinc-950 p-4 pb-12 font-sans">

  <!-- Modal de entrega -->
  <Transition name="fade">
    <div v-if="modalEntrega" class="fixed inset-0 z-50 flex items-end justify-center bg-black/70 backdrop-blur-sm" @click.self="modalEntrega = null">
      <div class="bg-zinc-900 border border-zinc-700 rounded-t-2xl w-full max-w-md p-6 pb-10">

        <p class="text-zinc-400 text-xs font-bold uppercase tracking-widest mb-1">Entregar moto</p>
        <h2 class="text-3xl font-mono font-black text-zinc-100 mb-1">{{ modalEntrega.placa_moto }}</h2>
        <p class="text-zinc-500 text-sm mb-6">{{ modalEntrega.nombre_cliente }}</p>

        <label class="text-zinc-400 text-xs font-bold uppercase tracking-widest block mb-2">Total cobrado</label>
        <div class="flex items-center gap-2 bg-zinc-800 border-2 border-zinc-600 focus-within:border-amber-500 rounded-xl px-4 py-3 mb-6 transition-colors">
          <span class="text-zinc-400 font-bold text-xl">$</span>
          <input
            ref="inputTotal"
            v-model="totalModal"
            type="number"
            min="0"
            step="0.01"
            inputmode="decimal"
            class="bg-transparent text-zinc-100 text-2xl font-mono font-bold w-full outline-none"
            placeholder="0.00"
          >
        </div>

        <button
          @click="confirmarEntrega"
          :disabled="entregando"
          class="w-full bg-emerald-600 hover:bg-emerald-500 active:bg-emerald-700 disabled:opacity-50 text-zinc-950 font-black py-4 rounded-xl text-sm tracking-wider uppercase transition-all"
        >
          {{ entregando ? 'Guardando...' : 'Confirmar entrega' }}
        </button>

      </div>
    </div>
  </Transition>
    
    <div class="mb-8 mt-2">
      <h1 class="text-3xl font-black text-zinc-100 tracking-tight uppercase">{{ nombreTaller }}</h1>
      <p class="text-zinc-400 font-medium mt-1 tracking-wide text-sm mb-4">CONTROL DE OPERACIONES</p>

      <div class="flex justify-between items-center">
        <!-- Secundarios: ícono solamente -->
        <div class="flex gap-2">
          <button @click="router.push('/metricas')" class="bg-zinc-800 hover:bg-zinc-700 active:bg-zinc-600 text-zinc-400 p-3 rounded-xl border border-zinc-700 transition-all" title="Métricas">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
            </svg>
          </button>
          <button @click="router.push('/historial')" class="bg-zinc-800 hover:bg-zinc-700 active:bg-zinc-600 text-zinc-400 p-3 rounded-xl border border-zinc-700 transition-all" title="Archivo">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0M12 12.75h.008v.008H12v-.008z" />
            </svg>
          </button>
          <button @click="logout" class="bg-zinc-800 hover:bg-red-900/50 active:bg-red-900 text-zinc-600 hover:text-red-400 p-3 rounded-xl border border-zinc-700 hover:border-red-800 transition-all" title="Cerrar sesión">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9" />
            </svg>
          </button>
        </div>

        <!-- Primario: ancho, con texto, bien visible -->
        <button @click="router.push('/registro')" class="flex items-center gap-2 bg-amber-500 hover:bg-amber-400 active:bg-amber-600 text-zinc-950 px-5 py-3 rounded-xl font-black text-sm uppercase tracking-wider shadow-[0_0_20px_rgba(245,158,11,0.25)] transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          Ingresar Moto
        </button>
      </div>
    </div>

    <div v-if="cargando" class="flex flex-col items-center justify-center mt-20">
      <div class="animate-spin rounded-full h-10 w-10 border-b-4 border-amber-500 mb-4"></div>
      <p class="text-zinc-500 font-medium uppercase tracking-widest text-sm">Cargando flota...</p>
    </div>

    <div v-else class="space-y-10">
      
      <section>
        <div class="flex items-center gap-3 mb-4 border-b border-zinc-800 pb-3">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6 text-amber-500">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.43l-1.003.767a1.123 1.123 0 0 0-.417 1.03c.004.074.006.148.006.222 0 .074-.002.148-.006.222a1.123 1.123 0 0 0 .417 1.03l1.003.767a1.125 1.125 0 0 1 .26 1.43l-1.296 2.247a1.125 1.125 0 0 1-1.37.49l-1.216-.456a1.125 1.125 0 0 0-1.076.124a6.57 6.57 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281a1.125 1.125 0 0 0-.646-.87a6.57 6.57 0 0 1-.22-.127c-.324-.196-.72-.257-1.075-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.43l1.004-.767a1.122 1.122 0 0 0 .416-1.03c-.004-.074-.006-.148-.006-.222 0-.074.002-.148.006-.222a1.122 1.122 0 0 0-.416-1.03l-1.004-.767a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.49l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128c.332-.183.582-.495.645-.869l.214-1.28Z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
          </svg>
          <h2 class="text-lg font-bold text-zinc-200 uppercase tracking-widest">En Taller</h2>
          <span class="bg-amber-500/10 text-amber-500 border border-amber-500/20 px-2.5 py-0.5 rounded text-xs font-bold ml-2">
            {{ ordenesEnTaller.length }}
          </span>
        </div>

        <div v-if="ordenesEnTaller.length === 0" class="text-center py-8 bg-zinc-900 rounded-xl border border-dashed border-zinc-700">
          <p class="text-zinc-500 text-sm">No hay motocicletas en reparación.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div 
            v-for="orden in ordenesEnTaller" 
            :key="orden.id"
            @click="irAlMuro(orden.id)"
            class="bg-zinc-900 p-5 rounded-xl border border-zinc-700 cursor-pointer hover:border-amber-500 active:bg-zinc-800 transition-all relative overflow-hidden group"
          >
            <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-amber-500 group-hover:w-2 transition-all"></div>
            
            <div class="flex justify-between items-start pl-2">
              <div>
                <h3 class="text-3xl font-mono font-black text-zinc-100 tracking-tight">{{ orden.placa_moto || 'S/P' }}</h3>
                <p class="text-zinc-400 text-sm font-medium mt-1 uppercase tracking-wide">{{ orden.modelo_moto }}</p>
              </div>
              <span class="text-[10px] font-bold text-zinc-500 bg-zinc-800 border border-zinc-700 px-2 py-1 rounded uppercase">
                #{{ orden.id }}
              </span>
            </div>
            
            <div class="mt-5 pt-4 border-t border-zinc-800 flex justify-between items-center pl-2 text-sm">
              <div class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 text-zinc-500">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
                <span class="font-bold text-zinc-300">{{ orden.nombre_cliente }}</span>
              </div>
              <span class="text-amber-500 text-xs font-bold bg-amber-500/10 px-2 py-1 rounded">
                {{ calcularDias(orden.fecha_ingreso) }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div class="flex items-center gap-3 mb-4 border-b border-zinc-800 pb-3">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6 text-emerald-500">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2 class="text-lg font-bold text-zinc-200 uppercase tracking-widest">Listas para Entrega</h2>
          <span class="bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 px-2.5 py-0.5 rounded text-xs font-bold ml-2">
            {{ ordenesListas.length }}
          </span>
        </div>

        <div v-if="ordenesListas.length === 0" class="text-center py-8 bg-zinc-900 rounded-xl border border-dashed border-zinc-700">
          <p class="text-zinc-500 text-sm">No hay motocicletas esperando retiro.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div 
            v-for="orden in ordenesListas" 
            :key="orden.id"
            @click="irAlMuro(orden.id)"
            class="bg-zinc-900 p-5 rounded-xl border border-zinc-700 cursor-pointer hover:border-emerald-500 active:bg-zinc-800 transition-all relative overflow-hidden group flex flex-col justify-between"
          >
            <div>
              <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-emerald-500 group-hover:w-2 transition-all"></div>
              
              <div class="flex justify-between items-start pl-2">
                <div>
                  <h3 class="text-3xl font-mono font-black text-zinc-100 tracking-tight">{{ orden.placa_moto || 'S/P' }}</h3>
                  <p class="text-zinc-400 text-sm font-medium mt-1 uppercase tracking-wide">{{ orden.modelo_moto }}</p>
                </div>
                <span class="text-[10px] font-bold text-zinc-500 bg-zinc-800 border border-zinc-700 px-2 py-1 rounded uppercase">
                  #{{ orden.id }}
                </span>
              </div>
              
              <div class="mt-5 pt-4 border-t border-zinc-800 flex justify-between items-center pl-2 text-sm">
                <div class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 text-zinc-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                  </svg>
                  <span class="font-bold text-zinc-300">{{ orden.nombre_cliente }}</span>
                </div>
                <span class="text-emerald-500 text-xs font-bold bg-emerald-500/10 px-2 py-1 rounded">
                  {{ calcularDias(orden.fecha_ingreso) }}
                </span>
              </div>
            </div>

            <button 
              @click.stop="entregarYArchivarOrden(orden)"
              class="w-full mt-5 bg-emerald-600 hover:bg-emerald-500 active:bg-emerald-700 text-zinc-950 font-black py-3 px-4 rounded-lg transition-all text-xs tracking-wider uppercase flex items-center justify-center gap-2 shadow-lg shadow-emerald-900/20"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
              </svg>
              Entregar Moto
            </button>

          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { useRouter } from 'vue-router';

const nombreTaller = import.meta.env.VITE_NOMBRE_TALLER || 'Taller Automotriz';

const router = useRouter();
const ordenes = ref([]);
const cargando = ref(true);
const modalEntrega = ref(null);
const totalModal = ref('');
const entregando = ref(false);
const inputTotal = ref(null);

function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  router.push('/login');
}

const ordenesEnTaller = computed(() => {
  return ordenes.value.filter(orden => orden.estado === 'taller');
});

const ordenesListas = computed(() => {
  return ordenes.value.filter(orden => orden.estado === 'lista');
});

const irAlMuro = (idOrden) => {
  router.push(`/muro/${idOrden}`);
};

const calcularDias = (fechaString) => {
  if (!fechaString) return 'Hoy';
  const fechaIngreso = new Date(fechaString);
  const hoy = new Date();
  const diferenciaTiempo = Math.abs(hoy - fechaIngreso);
  const diferenciaDias = Math.floor(diferenciaTiempo / (1000 * 60 * 60 * 24)); 
  
  if (diferenciaDias === 0) return 'Hoy';
  if (diferenciaDias === 1) return 'Hace 1 día';
  return `Hace ${diferenciaDias} días`;
};

const cargarFlota = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/ordenes/`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    });

    // Condición de seguridad para expulsar si el token caducó (Error 401)
    if (response.status === 401) {
      alert("Tu sesión ha caducado. Por favor, inicia sesión nuevamente.");
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      router.push('/login'); // Expulsa al usuario al login
      return; // Detiene la ejecución para que no intente cargar datos vacíos
    }

    if (response.ok) {
      const data = await response.json();
      ordenes.value = data.sort((a, b) => new Date(b.fecha_ingreso) - new Date(a.fecha_ingreso));
    }
  } catch (error) {
    console.error("Error al cargar el Kanban:", error);
  } finally {
    cargando.value = false;
  }
};

const entregarYArchivarOrden = (orden) => {
  totalModal.value = orden.total_cobro > 0 ? String(orden.total_cobro) : '';
  modalEntrega.value = orden;
  nextTick(() => inputTotal.value?.focus());
};

const confirmarEntrega = async () => {
  if (!modalEntrega.value) return;
  entregando.value = true;
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/motos/entregar/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
      body: JSON.stringify({ orden_id: modalEntrega.value.id, total_cobro: parseFloat(totalModal.value) || 0 }),
    });

    if (response.ok) {
      ordenes.value = ordenes.value.filter(o => o.id !== modalEntrega.value.id);
      modalEntrega.value = null;
    } else {
      const err = await response.json();
      alert('Error: ' + (err.error || 'Desconocido'));
    }
  } catch {
    alert('Problema de conexión con el servidor.');
  } finally {
    entregando.value = false;
  }
};

onMounted(() => {
  cargarFlota();
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>