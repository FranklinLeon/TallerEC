<template>
  <div class="min-h-screen bg-zinc-950 w-full font-sans">
    
    <div class="max-w-md md:max-w-2xl mx-auto p-4 pb-12">
      
      <div v-if="cargando" class="flex flex-col items-center justify-center mt-40">
        <div class="relative">
          <div class="animate-spin rounded-full h-14 w-14 border-4 border-zinc-800 border-t-amber-500"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="h-6 w-6 bg-amber-500 rounded-full animate-pulse opacity-20"></div>
          </div>
        </div>
        <p class="text-zinc-500 font-bold uppercase tracking-widest mt-6 text-xs animate-pulse">Conectando con el taller...</p>
      </div>

      <div v-else-if="error" class="bg-red-500/10 p-8 rounded-2xl border border-red-500/20 mt-12 text-center shadow-lg">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-16 h-16 text-red-500 mx-auto mb-4 opacity-80">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h3 class="text-red-400 font-black text-xl mb-2 uppercase tracking-wide">Enlace Caducado</h3>
        <p class="text-red-300/70 text-sm font-medium">El enlace de seguimiento es inválido o la orden ya fue archivada en {{ nombreTaller }}.</p>
      </div>

      <div v-else>
        
        <div class="bg-zinc-900 p-6 rounded-3xl shadow-[0_10px_30px_rgba(0,0,0,0.5)] border border-zinc-800 mb-10 mt-2 relative overflow-hidden">
          
          <div class="absolute top-0 left-0 w-full h-1" :class="orden.estado === 'taller' ? 'bg-amber-500' : 'bg-emerald-500'"></div>

          <div class="flex justify-between items-start">
            <div>
              <div class="flex items-center gap-2 mb-2">
                <span class="relative flex h-2.5 w-2.5">
                  <span v-if="orden.estado === 'taller'" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2.5 w-2.5" :class="orden.estado === 'taller' ? 'bg-amber-500' : 'bg-emerald-500'"></span>
                </span>
                <span class="text-[10px] font-bold uppercase tracking-widest text-zinc-400">
                  Reporte en Vivo
                </span>
              </div>
              
              <h2 class="text-4xl font-mono font-black text-zinc-100 mt-1 uppercase tracking-tight">
                {{ orden.placa_moto || 'S/P' }}
              </h2>
              <p class="text-zinc-400 font-medium text-sm mt-1 uppercase tracking-wide">
                {{ orden.modelo_moto }}
              </p>
            </div>
            <span class="px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest shadow-inner"
                  :class="orden.estado === 'taller' ? 'bg-amber-500/10 text-amber-500 border border-amber-500/20' : 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20'">
              {{ orden.estado }}
            </span>
          </div>
          
          <div class="border-t border-zinc-800 mt-5 pt-4 flex justify-between text-xs text-zinc-500">
            <div>
              <span class="block text-[10px] uppercase font-bold text-zinc-600 tracking-widest mb-1">Propietario</span>
              <span class="font-bold text-zinc-200 text-sm mt-0.5 block">
                {{ orden.nombre_cliente }}
              </span>
            </div>
            <div class="text-right">
              <span class="block text-[10px] uppercase font-bold text-zinc-600 tracking-widest mb-1">Ingreso</span>
              <span class="font-medium text-zinc-400 mt-0.5 block">
                {{ orden.fecha_ingreso ? new Date(orden.fecha_ingreso).toLocaleDateString('es-EC', { day: '2-digit', month: 'short', year: 'numeric' }) : '--/--/--' }}
              </span>
            </div>
          </div>
        </div>

        <!-- SECCIÓN DE COTIZACIONES -->
        <div v-if="orden.cotizacion && orden.cotizacion.length" class="mb-8 space-y-5">
          <div class="flex items-center gap-3 border-b border-zinc-800 pb-3">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-zinc-500">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="font-black text-zinc-200 text-sm uppercase tracking-widest">Autorizaciones del Taller</h3>
          </div>

          <div v-for="cot in orden.cotizacion" :key="cot.id" class="rounded-2xl border overflow-hidden"
               :class="{
                 'border-amber-500/30 bg-amber-500/5': cot.estado === 'pendiente',
                 'border-emerald-500/20 bg-zinc-900': cot.estado === 'aprobada',
                 'border-red-500/20 bg-zinc-900': cot.estado === 'rechazada',
               }">

            <div class="flex items-center justify-between px-5 py-3 border-b"
                 :class="{
                   'border-amber-500/20': cot.estado === 'pendiente',
                   'border-emerald-500/10': cot.estado === 'aprobada',
                   'border-red-500/10': cot.estado === 'rechazada',
                 }">
              <span class="text-zinc-400 text-[10px] font-bold uppercase tracking-widest">Cotización #{{ cot.id }}</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-widest"
                    :class="{
                      'bg-amber-500/20 text-amber-400': cot.estado === 'pendiente',
                      'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20': cot.estado === 'aprobada',
                      'bg-red-500/10 text-red-400 border border-red-500/20': cot.estado === 'rechazada',
                    }">
                {{ cot.estado }}
              </span>
            </div>

            <div class="px-5 pt-4 pb-2">
              <p v-if="cot.contexto" class="text-zinc-300 text-sm leading-relaxed italic mb-3">{{ cot.contexto }}</p>
              <img v-if="cot.foto_evidencia" :src="getFullUrl(cot.foto_evidencia)" class="rounded-xl w-full max-h-52 object-cover border border-zinc-700 mb-3" alt="Evidencia" />
            </div>

            <div class="border-t border-zinc-800/50">
              <div v-for="item in cot.items" :key="item.id" class="flex justify-between items-center px-5 py-3 border-b border-zinc-800/40 last:border-b-0">
                <span class="text-zinc-300 text-sm">{{ item.descripcion }}</span>
                <span class="text-zinc-100 font-mono font-bold text-sm">${{ Number(item.precio).toFixed(2) }}</span>
              </div>
              <div class="flex justify-between items-center px-5 py-3 bg-zinc-800/30">
                <span class="text-zinc-500 font-bold text-xs uppercase tracking-widest">Total</span>
                <span class="text-amber-400 font-mono font-black text-lg">${{ cot.total.toFixed(2) }}</span>
              </div>
            </div>

            <div v-if="cot.estado === 'pendiente'" class="flex gap-3 p-4">
              <button @click="responderCotizacion(cot, 'rechazada')" :disabled="respondiendo" class="flex-1 py-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 font-bold text-sm uppercase tracking-widest transition-all active:scale-[0.98] disabled:opacity-50">
                Rechazar
              </button>
              <button @click="responderCotizacion(cot, 'aprobada')" :disabled="respondiendo" class="flex-1 py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-zinc-950 font-black text-sm uppercase tracking-widest shadow-lg transition-all active:scale-[0.98] disabled:opacity-50">
                Aprobar
              </button>
            </div>
            <div v-else-if="cot.estado === 'aprobada'" class="flex items-center justify-center gap-2 py-3 mx-4 mb-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400 font-bold text-xs uppercase tracking-widest">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              Autorizado
            </div>
            <div v-else-if="cot.estado === 'rechazada'" class="flex items-center justify-center gap-2 py-3 mx-4 mb-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 font-bold text-xs uppercase tracking-widest">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
              Rechazado
            </div>

          </div>
        </div>

        <div class="flex items-center gap-3 mb-6 border-b border-zinc-800 pb-3">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-zinc-500">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="font-black text-zinc-200 text-sm uppercase tracking-widest">Historial de Mantenimiento</h3>
        </div>

        <div class="relative border-l-2 border-zinc-800 ml-3 mt-4 md:ml-6" v-if="orden.eventos && orden.eventos.length > 0">
          <div v-for="(evento, index) in orden.eventos" :key="evento.id" class="mb-8 ml-6">
            
            <div v-if="esNuevoDia(index)" class="flex justify-center mb-8 -ml-9 relative z-10 mt-6">
               <span class="bg-zinc-900 text-zinc-400 border border-zinc-700 text-[10px] font-bold px-4 py-1.5 rounded shadow-sm uppercase tracking-widest">
                 {{ formatearFechaSeparador(evento.fecha) }}
               </span>
            </div>

            <template v-if="evento.contenido_texto && evento.contenido_texto.includes('Trabajo finalizado')">
              <span class="absolute flex items-center justify-center w-3 h-3 bg-zinc-600 rounded-full -left-[7px] ring-4 ring-zinc-950 z-10 mt-5"></span>
              <div class="border-t-2 border-dashed border-zinc-700 w-full pt-4 mt-6 mb-2">
                <div class="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-4 py-3 rounded-xl border border-emerald-500/20 shadow-sm">
                  <span class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Trabajo Finalizado
                  </span>
                  <span class="font-mono text-[10px] text-emerald-500/70">{{ formatearHora(evento.fecha) }}</span>
                </div>
              </div>
            </template>

            <template v-else>
              <span class="absolute flex items-center justify-center w-3 h-3 bg-amber-500 rounded-full -left-[7px] ring-4 ring-zinc-950 z-10 mt-1.5"></span>
              <h3 class="font-bold text-zinc-600 uppercase mb-2 text-[10px] tracking-widest">{{ evento.tipo }}</h3>
              
              <div v-if="evento.tipo === 'tarea'" 
                   class="flex items-center p-4 bg-zinc-900 border rounded-xl shadow-sm transition-all relative mt-1"
                   :class="evento.completada ? 'border-emerald-500/20 bg-emerald-500/5' : 'border-zinc-800'">
                
                <div class="relative w-6 h-6 mr-4 flex-shrink-0">
                  <div class="w-full h-full rounded-full border-2 flex items-center justify-center transition-colors"
                       :class="evento.completada ? 'bg-emerald-500 border-emerald-500' : 'border-zinc-700 bg-zinc-800'">
                    <svg v-if="evento.completada" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-zinc-950" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>

                <span class="text-sm flex-1 pr-8 leading-tight transition-all" :class="evento.completada ? 'text-zinc-500' : 'text-zinc-200 font-medium'">
                  {{ evento.contenido_texto }}
                </span>
                <span class="text-[10px] text-zinc-600 font-mono absolute bottom-2 right-3">
                  {{ formatearHora(evento.fecha) }}
                </span>
              </div>

              <div v-else-if="evento.contenido_texto" class="bg-zinc-800/50 p-4 rounded-xl mt-1 shadow-sm border border-zinc-700 relative pb-8">
                <p class="text-zinc-300 text-sm leading-relaxed">{{ evento.contenido_texto }}</p>
                <span class="text-[10px] text-zinc-500 font-mono absolute bottom-2 right-3">
                  {{ formatearHora(evento.fecha) }}
                </span>
              </div>

              <div v-if="evento.archivo" class="relative inline-block mt-2">
                <img :src="getFullUrl(evento.archivo)" class="rounded-xl shadow-lg w-full max-w-xs border border-zinc-700 object-cover" alt="Evidencia de mantenimiento" />
                <span class="text-[10px] text-zinc-100 bg-zinc-950/80 px-2 py-1 rounded font-mono absolute bottom-3 right-3 z-10 backdrop-blur-sm">
                  {{ formatearHora(evento.fecha) }}
                </span>
              </div>
            </template>
          </div>
        </div>
        
        <div v-else class="text-center py-12 bg-zinc-900 rounded-2xl border border-dashed border-zinc-800 mt-6 shadow-inner">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 text-zinc-700 mx-auto mb-3">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-zinc-500 text-sm tracking-wide">El taller está preparando tu motocicleta.</p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const HASH_SEGUIMIENTO = route.params.hash;

const orden = ref(null);
const cargando = ref(true);
const error = ref(false);
const API_URL = import.meta.env.VITE_API_URL;
const nombreTaller = import.meta.env.VITE_NOMBRE_TALLER || 'Taller Automotriz';

let pollingInterval = null;
const respondiendo = ref(false);

const responderCotizacion = async (cotizacion, respuesta) => {
  if (!confirm(respuesta === 'aprobada' ? '¿Aprobar esta cotización?' : '¿Rechazar esta cotización?')) return;
  respondiendo.value = true;
  try {
    const response = await fetch(`${API_URL}/cotizacion/${cotizacion.id}/responder/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ respuesta })
    });
    if (response.ok) await cargarSeguimiento();
  } catch (err) {
    console.error('Error al responder cotización:', err);
  } finally {
    respondiendo.value = false;
  }
};

// ---> AQUÍ ESTÁ LA FUNCIÓN MODIFICADA <---
const getFullUrl = (path) => {
  if (!path) return '';
  const urlBase = API_URL.replace('/api', '');
  
  if (path.startsWith('http')) {
    try {
      const urlObj = new URL(path);
      return `${urlBase}${urlObj.pathname}`;
    } catch (e) {
      return path;
    }
  }
  
  return `${urlBase}${path}`;
};
// ------------------------------------------

const cargarSeguimiento = async () => {
  try {
    const response = await fetch(`${API_URL}/seguimiento/${HASH_SEGUIMIENTO}/`);
    
    if (response.ok) {
      const data = await response.json();
      
      if (data.eventos && data.eventos.length > 0) {
        data.eventos.sort((a, b) => a.id - b.id);
      }
      
      orden.value = data;
      error.value = false;
    } else {
      error.value = true;
    }
  } catch (err) {
    console.error("Error al cargar el seguimiento:", err);
    error.value = true;
  } finally {
    cargando.value = false;
  }
};

const esNuevoDia = (index) => {
  if (!orden.value.eventos) return false;
  if (index === 0) return true;
  const fechaActual = new Date(orden.value.eventos[index].fecha).toDateString();
  const fechaAnterior = new Date(orden.value.eventos[index - 1].fecha).toDateString();
  return fechaActual !== fechaAnterior;
};

const formatearFechaSeparador = (fechaString) => {
  if (!fechaString) return '';
  const fecha = new Date(fechaString);
  const hoy = new Date();
  const ayer = new Date(hoy);
  ayer.setDate(ayer.getDate() - 1);
  if (fecha.toDateString() === hoy.toDateString()) return 'Hoy';
  if (fecha.toDateString() === ayer.toDateString()) return 'Ayer';
  return fecha.toLocaleDateString('es-EC', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
};

const formatearHora = (fechaString) => {
  if (!fechaString) return '';
  return new Date(fechaString).toLocaleTimeString('es-EC', { hour: '2-digit', minute: '2-digit', hour12: true });
};

onMounted(() => {
  cargarSeguimiento();
  pollingInterval = setInterval(cargarSeguimiento, 10000);
});

onUnmounted(() => {
  if (pollingInterval) clearInterval(pollingInterval);
});
</script>