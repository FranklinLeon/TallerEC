<template>
  <div class="min-h-screen bg-zinc-950 w-full font-sans">
    
    <div class="max-w-md md:max-w-2xl mx-auto p-4 pb-32 relative">
      
      <div class="flex items-center mb-2 mt-2">
        <button @click="irAlMenuPrincipal" class="text-zinc-500 hover:text-zinc-300 transition-colors p-2 -ml-2 rounded-lg active:bg-zinc-800 flex items-center gap-1 text-sm font-bold">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
          Volver
        </button>
      </div>

      <div v-if="orden" class="bg-zinc-900 p-5 rounded-2xl shadow-xl border border-zinc-800 mb-8 relative overflow-hidden">
        <div class="absolute left-0 top-0 bottom-0 w-1.5" :class="orden.estado === 'taller' ? 'bg-amber-500' : 'bg-emerald-500'"></div>

        <div class="flex justify-between items-start pl-2">
          <div>
            <span class="text-[10px] font-bold uppercase tracking-widest text-zinc-500 bg-zinc-800 border border-zinc-700 px-2 py-0.5 rounded">
              Orden #{{ ORDEN_TRABAJO_ID }}
            </span>
            <h2 class="text-3xl font-mono font-black text-zinc-100 mt-2 uppercase tracking-tight">
              {{ orden.placa_moto || 'S/P' }}
            </h2>
            <p class="text-zinc-400 font-medium text-sm mt-1 uppercase tracking-wide">
              {{ orden.modelo_moto || 'Especificación de Motocicleta' }}
            </p>
          </div>
          <span class="px-3 py-1 rounded text-[10px] font-bold uppercase tracking-widest"
                :class="orden.estado === 'taller' ? 'bg-amber-500/10 text-amber-500 border border-amber-500/20' : 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20'">
            {{ orden.estado }}
          </span>
        </div>
        
        <div class="border-t border-zinc-800 mt-4 pt-4 flex justify-between text-xs text-zinc-500 pl-2">
          <div>
            <span class="block text-[10px] uppercase font-bold text-zinc-600 tracking-widest mb-1">Cliente</span>
            <div class="flex items-center gap-1.5">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 text-zinc-400">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
              <span class="font-bold text-zinc-200 text-sm block">
                {{ orden.nombre_cliente || 'Registrado' }}
              </span>
            </div>
          </div>
          <div class="text-right">
            <span class="block text-[10px] uppercase font-bold text-zinc-600 tracking-widest mb-1">Ingreso</span>
            <span class="font-medium text-zinc-400 text-sm block">
              {{ orden.fecha_ingreso ? new Date(orden.fecha_ingreso).toLocaleDateString('es-EC', { day: '2-digit', month: 'short' }) : '--/--' }}
            </span>
          </div>
        </div>

        <div v-if="cotizaciones.length" class="mt-3 pt-3 border-t border-zinc-800 pl-2 flex items-center justify-between">
          <span class="text-[10px] uppercase font-bold text-zinc-600 tracking-widest">Cotizaciones</span>
          <div class="flex items-center gap-1.5">
            <span v-for="c in cotizaciones" :key="c.id"
                  class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-widest"
                  :class="{
                    'bg-amber-500/10 text-amber-500 border border-amber-500/20': c.estado === 'pendiente',
                    'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20': c.estado === 'aprobada',
                    'bg-red-500/10 text-red-500 border border-red-500/20': c.estado === 'rechazada',
                  }">
              ${{ c.total.toFixed(2) }}
            </span>
          </div>
        </div>
      </div>

      <div class="relative border-l-2 border-zinc-800 ml-3 mt-4 md:ml-6">
        <div v-for="(evento, index) in eventos" :key="evento.id" class="mb-8 ml-6">
          
          <div v-if="esNuevoDia(index)" class="flex justify-center mb-8 -ml-9 relative z-10 mt-6">
             <span class="bg-zinc-800 text-zinc-400 border border-zinc-700 text-[10px] uppercase tracking-widest font-bold px-4 py-1.5 rounded shadow-sm">
               {{ formatearFechaSeparador(evento.fecha) }}
             </span>
          </div>

          <template v-if="evento.contenido_texto && evento.contenido_texto.includes('Trabajo finalizado')">
            <span class="absolute flex items-center justify-center w-3 h-3 bg-zinc-500 rounded-full -left-[7px] ring-4 ring-zinc-950 z-10 mt-5"></span>
            <div class="border-t-2 border-dashed border-zinc-700 w-full pt-4 mt-6 mb-2">
              <div class="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-4 py-3 rounded-xl border border-emerald-500/20 shadow-sm">
                <span class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Orden Clausurada
                </span>
                <span class="font-mono text-[10px] text-emerald-500/70">{{ formatearHora(evento.fecha) }}</span>
              </div>
            </div>
          </template>

          <template v-else>
            <span class="absolute flex items-center justify-center w-3 h-3 rounded-full -left-[7px] ring-4 ring-zinc-950 z-10 mt-1.5"
                  :class="esMensajeCliente(evento.contenido_texto) ? 'bg-[#25D366]' : 'bg-blue-500'"></span>
            
            <h3 class="font-bold uppercase mb-2 text-[10px] tracking-widest"
                :class="esMensajeCliente(evento.contenido_texto) ? 'text-[#25D366]' : 'text-zinc-600'">
              {{ esMensajeCliente(evento.contenido_texto) ? 'Mensaje del Cliente' : evento.tipo }}
            </h3>
            
            <div v-if="evento.tipo === 'tarea'" 
                 class="flex items-center p-4 bg-zinc-900 border rounded-xl shadow-sm transition-all relative mt-1 group"
                 :class="evento.completada ? 'border-emerald-500/30 bg-emerald-500/5 opacity-50' : 'border-zinc-700 hover:border-zinc-500'">
              
              <template v-if="editandoId !== evento.id">
                <div class="relative w-7 h-7 mr-4 flex-shrink-0 cursor-pointer">
                  <input type="checkbox" v-model="evento.completada" @change="actualizarEstadoTarea(evento)" class="opacity-0 absolute w-full h-full z-10 cursor-pointer">
                  <div class="w-full h-full rounded border-2 flex items-center justify-center transition-colors"
                       :class="evento.completada ? 'bg-emerald-500 border-emerald-500' : 'border-zinc-600 bg-zinc-800'">
                    <svg v-if="evento.completada" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-zinc-950" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>

                <span class="text-base flex-1 pr-14 leading-tight transition-all" :class="evento.completada ? 'line-through text-zinc-500' : 'text-zinc-200 font-medium'">
                  {{ evento.contenido_texto }}
                </span>
                <span class="text-[10px] text-zinc-600 font-mono absolute bottom-2 right-3">
                  {{ formatearHora(evento.fecha) }}
                </span>
                
                <div class="absolute top-2 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                   <button @click="iniciarEdicionTexto(evento)" class="p-1.5 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 rounded transition-colors">
                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" /></svg>
                   </button>
                   <button @click="confirmarEliminacion(evento.id)" class="p-1.5 text-red-500 hover:text-red-400 hover:bg-red-500/10 rounded transition-colors">
                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>
                   </button>
                </div>
              </template>

              <template v-else>
                <input type="text" v-model="textoEditado" class="w-full border-b-2 border-amber-500 bg-zinc-950 p-2 text-base text-zinc-100 focus:outline-none rounded" autofocus>
                <div class="flex flex-col gap-1 ml-2">
                  <button @click="guardarEdicionTexto(evento)" class="p-2 bg-emerald-500 text-zinc-950 rounded shadow-sm text-xs font-bold">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg>
                  </button>
                  <button @click="cancelarEdicion" class="p-2 bg-zinc-600 text-zinc-100 rounded shadow-sm text-xs font-bold">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                  </button>
                </div>
              </template>
            </div>

            <!-- Tarjeta cotización enviada -->
            <div v-else-if="esCotizacionEnviada(evento.contenido_texto)" class="mt-1 rounded-xl border border-amber-500/30 bg-amber-500/5 overflow-hidden">
              <div class="flex items-center justify-between px-4 py-2.5 border-b border-amber-500/20">
                <span class="text-amber-400 text-[10px] font-black uppercase tracking-widest">Cotización enviada</span>
                <span class="text-amber-400 font-mono font-black text-sm">${{ parsearCotizacionEnviada(evento.contenido_texto).total }}</span>
              </div>
              <p class="text-zinc-400 text-xs px-4 py-2.5 leading-relaxed italic">{{ parsearCotizacionEnviada(evento.contenido_texto).contexto }}</p>
              <span class="text-[10px] text-zinc-600 font-mono px-4 pb-2 block">{{ formatearHora(evento.fecha) }}</span>
            </div>

            <!-- Tarjeta cotización aprobada -->
            <div v-else-if="esCotizacionAprobada(evento.contenido_texto)" class="mt-1 flex items-center gap-3 px-4 py-3 rounded-xl border border-emerald-500/30 bg-emerald-500/5">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5 text-emerald-400 flex-shrink-0"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <div class="flex-1">
                <p class="text-emerald-400 text-xs font-black uppercase tracking-widest">Cliente autorizó</p>
                <p class="text-zinc-500 text-[10px] font-mono mt-0.5">{{ formatearHora(evento.fecha) }}</p>
              </div>
            </div>

            <!-- Tarjeta cotización rechazada -->
            <div v-else-if="esCotizacionRechazada(evento.contenido_texto)" class="mt-1 flex items-center gap-3 px-4 py-3 rounded-xl border border-red-500/30 bg-red-500/5">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5 text-red-400 flex-shrink-0"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <div class="flex-1">
                <p class="text-red-400 text-xs font-black uppercase tracking-widest">Cliente rechazó</p>
                <p class="text-zinc-500 text-[10px] font-mono mt-0.5">{{ formatearHora(evento.fecha) }}</p>
              </div>
            </div>

            <!-- Nota normal o mensaje del cliente -->
            <div v-else-if="evento.contenido_texto" class="p-4 rounded-xl mt-1 shadow-sm border relative pb-8 group"
                 :class="esMensajeCliente(evento.contenido_texto) ? 'bg-[#25D366]/10 border-[#25D366]/30' : 'bg-zinc-800/50 border-zinc-700'">
              <template v-if="editandoId !== evento.id">
                <p class="text-sm leading-relaxed pr-8"
                   :class="esMensajeCliente(evento.contenido_texto) ? 'text-zinc-200 italic font-medium' : 'text-zinc-300'">
                  {{ esMensajeCliente(evento.contenido_texto) ? limpiarMensajeCliente(evento.contenido_texto) : evento.contenido_texto }}
                </p>
                <span class="text-[10px] font-mono absolute bottom-2 right-3"
                      :class="esMensajeCliente(evento.contenido_texto) ? 'text-[#25D366]/70' : 'text-zinc-500'">
                  {{ formatearHora(evento.fecha) }}
                </span>
                <div class="absolute top-2 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                   <button @click="iniciarEdicionTexto(evento)" class="p-1.5 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-700 rounded transition-colors">
                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" /></svg>
                   </button>
                   <button @click="confirmarEliminacion(evento.id)" class="p-1.5 text-red-500 hover:text-red-400 hover:bg-red-500/10 rounded transition-colors">
                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>
                   </button>
                </div>
              </template>
              <template v-else>
                <textarea v-model="textoEditado" class="w-full border-2 border-amber-500 bg-zinc-950 p-3 rounded text-zinc-100 focus:outline-none text-sm" rows="3"></textarea>
                <div class="flex gap-2 justify-end mt-3">
                  <button @click="cancelarEdicion" class="px-4 py-2 bg-zinc-700 text-zinc-200 rounded font-bold text-xs uppercase tracking-widest">Cancelar</button>
                  <button @click="guardarEdicionTexto(evento)" class="px-4 py-2 bg-emerald-500 text-zinc-950 rounded font-bold text-xs uppercase tracking-widest">Guardar</button>
                </div>
              </template>
            </div>

            <div v-if="evento.archivo" class="relative inline-block mt-2 group">
              <img :src="obtenerUrlImagen(evento.archivo)" class="rounded-xl shadow-lg w-full max-w-xs border border-zinc-700" alt="Evidencia" />
              <span class="text-[10px] text-zinc-100 bg-zinc-950/80 px-2 py-1 rounded font-mono absolute bottom-3 right-3 z-10 backdrop-blur-sm">
                {{ formatearHora(evento.fecha) }}
              </span>
              
              <div class="absolute top-3 right-3 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity bg-zinc-900/80 p-1.5 rounded-lg backdrop-blur-sm border border-zinc-700">
                 <button @click="abrirCamara(evento.id)" class="p-1.5 text-blue-400 hover:text-blue-300 hover:bg-zinc-800 rounded transition-colors" title="Retomar foto">
                   <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" /></svg>
                 </button>
                 <button @click="confirmarEliminacion(evento.id)" class="p-1.5 text-red-500 hover:text-red-400 hover:bg-red-500/10 rounded transition-colors" title="Eliminar">
                   <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>
                 </button>
              </div>
            </div>
          </template>
        </div>
      </div>
    
      <div v-if="textoTranscrito" class="mt-6 p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl shadow-sm text-center mx-2 backdrop-blur-sm">
        <p class="text-amber-500 font-bold animate-pulse text-sm uppercase tracking-wider">{{ textoTranscrito }}</p>
      </div>

      <div v-if="orden && orden.estado === 'taller'" class="mt-12 mb-8 px-2">
        <button
          @click="abrirModalCierre"
          class="w-full bg-emerald-600 hover:bg-emerald-500 active:scale-[0.98] text-zinc-950 font-black py-4 px-4 rounded-xl transition-all text-sm shadow-lg shadow-emerald-900/30 flex items-center justify-center gap-3 tracking-widest uppercase border border-emerald-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Moto lista — Avisar al cliente
        </button>
      </div>

      <div v-if="orden && (orden.estado === 'lista' || orden.estado === 'entregada')" class="mt-12 mb-8 px-2">
        <button 
          @click="irAlMenuPrincipal" 
          class="w-full bg-zinc-800 hover:bg-zinc-700 active:scale-[0.98] text-zinc-200 font-bold py-4 px-4 rounded-xl transition-all text-sm shadow-lg border border-zinc-700 flex items-center justify-center gap-2 tracking-widest uppercase"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" />
          </svg>
          Volver al Tablero
        </button>
      </div>

      <transition name="fade">
        <button 
          v-if="mostrarBotonScroll" 
          @click="scrollToBottom" 
          class="fixed bottom-28 right-5 bg-zinc-800 text-zinc-300 p-3 rounded-full shadow-2xl z-40 border border-zinc-600 opacity-80 hover:opacity-100 transition-all backdrop-blur-md"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3" />
          </svg>
        </button>
      </transition>
      
    </div>

    <!-- MODAL CIERRE DE ORDEN -->
    <div v-if="mostrarModalCierre" class="fixed inset-0 bg-black/80 z-[70] flex items-end justify-center backdrop-blur-sm">
      <div class="bg-zinc-900 border border-zinc-700 rounded-t-3xl w-full max-w-lg shadow-2xl max-h-[85vh] flex flex-col">

        <div class="flex items-center justify-between p-5 border-b border-zinc-800">
          <div>
            <h3 class="text-zinc-100 font-black text-base uppercase tracking-widest">Resumen del trabajo</h3>
            <p class="text-zinc-500 text-xs mt-0.5">Se notificará al cliente por WhatsApp</p>
          </div>
          <button @click="mostrarModalCierre = false" class="text-zinc-400 hover:text-zinc-200 p-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>

        <div class="overflow-y-auto flex-1 p-5 space-y-3">

          <!-- Items de cotizaciones aprobadas (readonly) -->
          <template v-for="c in cotizaciones.filter(x => x.estado === 'aprobada')" :key="c.id">
            <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Cotización aprobada — ${{ c.total.toFixed(2) }}</p>
            <div v-for="item in c.items" :key="item.id" class="flex justify-between items-center px-3 py-2.5 bg-zinc-800/60 rounded-xl border border-zinc-700">
              <span class="text-zinc-300 text-sm">{{ item.descripcion }}</span>
              <span class="text-zinc-300 font-mono text-sm font-bold">${{ Number(item.precio).toFixed(2) }}</span>
            </div>
            <div class="border-t border-zinc-800 pt-2"></div>
          </template>

          <!-- Items adicionales editables -->
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Agregar conceptos</p>

          <div v-for="(item, index) in itemsCierre" :key="index" class="flex gap-2 items-center">
            <input
              v-model="item.descripcion"
              type="text"
              placeholder="Ej: Mano de obra, repuesto..."
              class="flex-1 bg-zinc-800 border border-zinc-700 rounded-xl px-3 py-2.5 text-zinc-100 text-sm focus:border-amber-500 focus:outline-none placeholder-zinc-600"
            />
            <div class="relative w-24">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500 text-sm font-mono">$</span>
              <input
                v-model="item.precio"
                type="number"
                min="0"
                step="0.01"
                inputmode="decimal"
                placeholder="0.00"
                class="w-full bg-zinc-800 border border-zinc-700 rounded-xl pl-6 pr-2 py-2.5 text-zinc-100 text-sm font-mono focus:border-amber-500 focus:outline-none"
              />
            </div>
            <button @click="eliminarItemCierre(index)" class="text-red-500 hover:text-red-400 p-1 flex-shrink-0" :disabled="itemsCierre.length === 1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>

          <button @click="itemsCierre.push({ descripcion: '', precio: '' })" class="w-full py-2.5 border border-dashed border-zinc-700 rounded-xl text-zinc-500 hover:text-zinc-300 hover:border-zinc-500 text-sm font-bold uppercase tracking-widest transition-colors flex items-center justify-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
            Agregar concepto
          </button>

        </div>

        <div class="p-5 border-t border-zinc-800">
          <div class="flex justify-between items-center mb-4">
            <span class="text-zinc-400 font-bold text-sm uppercase tracking-widest">Total</span>
            <span class="text-emerald-400 font-mono font-black text-2xl">${{ totalCierre.toFixed(2) }}</span>
          </div>
          <button
            @click="confirmarCierre"
            :disabled="cerrandoOrden"
            class="w-full py-4 bg-emerald-600 hover:bg-emerald-500 active:scale-[0.98] disabled:opacity-50 text-zinc-950 font-black rounded-xl text-sm uppercase tracking-widest transition-all flex items-center justify-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5"><path fill-rule="evenodd" d="M1.5 4.5a3 3 0 013-3h1.372c.86 0 1.61.586 1.819 1.42l1.105 4.423a1.875 1.875 0 01-.694 1.955l-1.293.97c-.135.101-.164.249-.126.352a11.285 11.285 0 006.697 6.697c.103.038.25.009.352-.126l.97-1.293a1.875 1.875 0 011.955-.694l4.423 1.105c.834.209 1.42.959 1.42 1.82V19.5a3 3 0 01-3 3h-2.25C8.552 22.5 1.5 15.448 1.5 6.75V4.5z" clip-rule="evenodd" /></svg>
            {{ cerrandoOrden ? 'Enviando...' : 'Avisar al cliente — WhatsApp' }}
          </button>
        </div>

      </div>
    </div>

    <!-- MODAL COTIZACIÓN -->
    <div v-if="mostrarModalCotizacion" class="fixed inset-0 bg-black/80 z-[70] flex items-end justify-center backdrop-blur-sm">
      <div class="bg-zinc-900 border border-zinc-700 rounded-t-3xl w-full max-w-lg shadow-2xl max-h-[85vh] flex flex-col">
        <div class="flex items-center justify-between p-5 border-b border-zinc-800">
          <h3 class="text-zinc-100 font-black text-base uppercase tracking-widest">Cotización</h3>
          <button @click="mostrarModalCotizacion = false" class="text-zinc-400 hover:text-zinc-200 p-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>

        <div class="overflow-y-auto flex-1 p-5 space-y-4">

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-widest mb-1.5">¿Qué se encontró? *</label>
            <textarea v-model="contextoCotizacion" rows="3" placeholder="Ej: Al desarmar el freno delantero se encontró que los discos están desgastados y necesitan reemplazo..." class="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-3 py-2.5 text-zinc-100 text-sm focus:border-amber-500 focus:outline-none placeholder-zinc-600 resize-none"></textarea>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-widest mb-1.5">Foto de evidencia (opcional)</label>
            <label class="flex items-center justify-center gap-2 w-full py-3 border border-dashed border-zinc-700 rounded-xl text-zinc-500 hover:text-zinc-300 hover:border-zinc-500 text-sm font-bold uppercase tracking-widest transition-colors cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              {{ fotoEvidencia ? 'Cambiar foto' : 'Tomar o subir foto' }}
              <input type="file" accept="image/*" capture="environment" class="hidden" @change="onFotoSeleccionada" />
            </label>
            <img v-if="fotoPreview" :src="fotoPreview" class="mt-2 rounded-xl w-full max-h-40 object-cover border border-zinc-700" />
          </div>

          <div class="border-t border-zinc-800 pt-3">
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-widest mb-2">Ítems y precios *</label>
          </div>

          <div v-for="(item, index) in itemsCotizacion" :key="index" class="flex gap-2 items-center">
            <input v-model="item.descripcion" type="text" placeholder="Descripción (ej: Cambio de aceite)" class="flex-1 bg-zinc-800 border border-zinc-700 rounded-xl px-3 py-2.5 text-zinc-100 text-sm focus:border-amber-500 focus:outline-none placeholder-zinc-600" />
            <div class="relative w-24">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500 text-sm font-mono">$</span>
              <input v-model="item.precio" type="number" min="0" step="0.01" placeholder="0.00" class="w-full bg-zinc-800 border border-zinc-700 rounded-xl pl-6 pr-2 py-2.5 text-zinc-100 text-sm font-mono focus:border-amber-500 focus:outline-none" />
            </div>
            <button @click="eliminarItem(index)" class="text-red-500 hover:text-red-400 p-1 flex-shrink-0" :disabled="itemsCotizacion.length === 1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>

          <button @click="agregarItem" class="w-full py-2.5 border border-dashed border-zinc-700 rounded-xl text-zinc-500 hover:text-zinc-300 hover:border-zinc-500 text-sm font-bold uppercase tracking-widest transition-colors flex items-center justify-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
            Agregar ítem
          </button>
        </div>

        <div class="p-5 border-t border-zinc-800">
          <div class="flex justify-between items-center mb-4">
            <span class="text-zinc-400 font-bold text-sm uppercase tracking-widest">Total</span>
            <span class="text-amber-500 font-mono font-black text-2xl">${{ totalCotizacion.toFixed(2) }}</span>
          </div>
          <button @click="enviarCotizacion" :disabled="enviandoCotizacion" class="w-full py-4 bg-amber-500 hover:bg-amber-400 active:scale-[0.98] text-zinc-950 font-black rounded-xl text-sm uppercase tracking-widest transition-all flex items-center justify-center gap-2 disabled:opacity-50">
            <svg v-if="!enviandoCotizacion" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5"><path d="M3.478 2.404a.75.75 0 00-.926.941l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.404z" /></svg>
            <span>{{ enviandoCotizacion ? 'Enviando...' : 'Enviar por WhatsApp' }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="mostrarModalConfirmacion" class="fixed inset-0 bg-black/80 z-[70] flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-zinc-900 border border-zinc-700 rounded-2xl p-6 max-w-sm w-full shadow-2xl">
        <h3 class="text-zinc-100 font-bold text-lg mb-2">Eliminar Registro</h3>
        <p class="text-zinc-400 text-sm mb-6">¿Borrar este elemento de forma permanente?</p>
        
        <div class="flex gap-3 justify-end">
          <button @click="cancelarEliminacion" class="px-5 py-2.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-xl font-bold text-xs uppercase tracking-widest transition-colors">
            Cancelar
          </button>
          <button @click="ejecutarEliminacion" class="px-5 py-2.5 bg-red-600/10 hover:bg-red-600/20 text-red-500 border border-red-500/30 rounded-xl font-bold text-xs uppercase tracking-widest transition-colors">
            Eliminar
          </button>
        </div>
      </div>
    </div>

    <div v-if="orden && orden.estado === 'taller'" class="fixed bottom-0 left-0 right-0 w-full max-w-md md:max-w-2xl mx-auto bg-zinc-950/90 border-t border-zinc-800 px-4 pt-4 pb-8 flex items-center gap-3 z-50 pb-safe shadow-[0_-10px_20px_rgba(0,0,0,0.5)] backdrop-blur-md">
      
      <div class="flex-1 bg-zinc-900 rounded-full flex items-center px-4 py-2.5 border border-zinc-700 focus-within:border-amber-500 transition-colors">
        <input 
          v-model="nuevoMensaje" 
          @keyup.enter="enviarNota"
          type="text" 
          placeholder="Escribir nota..." 
          class="w-full focus:outline-none text-zinc-200 bg-transparent text-sm placeholder-zinc-500" 
        />
        
        <button v-if="nuevoMensaje.trim().length > 0" @click="enviarNota" class="text-amber-500 p-1 hover:text-amber-400 transition-transform transform active:scale-90 flex-shrink-0 ml-2">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
            <path d="M3.478 2.404a.75.75 0 00-.926.941l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.404z" />
          </svg>
        </button>

        <button v-else @click="abrirCamara" class="text-zinc-400 p-1 hover:text-zinc-200 transition-transform transform active:scale-90 flex-shrink-0 ml-2" title="Tomar Foto">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </button>
      </div>

      <button @click="toggleRecording" :class="isRecording ? 'bg-red-600 text-white animate-pulse shadow-[0_0_20px_rgba(220,38,38,0.6)] scale-110' : 'bg-amber-500 text-zinc-950 hover:bg-amber-400'" class="p-4 rounded-full transition-all transform active:scale-95 flex-shrink-0">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
        </svg>
      </button>

      <button @click="abrirModalCotizacion" class="bg-zinc-700 hover:bg-zinc-600 text-zinc-200 p-4 rounded-full shadow-md transition-transform transform active:scale-90 flex-shrink-0" title="Cotización">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </button>

      <button @click="irAWhatsApp" class="bg-[#25D366] hover:bg-[#1ebd5a] text-white p-4 rounded-full shadow-md transition-transform transform active:scale-90 flex-shrink-0">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
          <path fill-rule="evenodd" d="M1.5 4.5a3 3 0 013-3h1.372c.86 0 1.61.586 1.819 1.42l1.105 4.423a1.875 1.875 0 01-.694 1.955l-1.293.97c-.135.101-.164.249-.126.352a11.285 11.285 0 006.697 6.697c.103.038.25.009.352-.126l.97-1.293a1.875 1.875 0 011.955-.694l4.423 1.105c.834.209 1.42.959 1.42 1.82V19.5a3 3 0 01-3 3h-2.25C8.552 22.5 1.5 15.448 1.5 6.75V4.5z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>

    <div v-show="mostrarCamara" class="fixed inset-0 bg-black z-[60] flex flex-col justify-between">
      <div class="flex justify-between items-center p-6 bg-gradient-to-b from-black/80 to-transparent">
        <span class="text-zinc-200 font-bold uppercase tracking-widest text-sm">{{ idFotoAEditar ? 'Reemplazar Evidencia' : 'Capturar Evidencia' }}</span>
        <button @click="cerrarCamara" class="text-zinc-200 p-2 hover:bg-white/10 rounded-full transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>
      
      <div class="flex-1 flex items-center justify-center relative overflow-hidden">
        <video ref="video" class="min-w-full min-h-full object-cover" autoplay playsinline></video>
        <canvas ref="canvas" class="hidden"></canvas>
        
        <div class="absolute inset-0 pointer-events-none border-[1px] border-white/20 m-8 rounded-2xl">
          <div class="absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 border-amber-500 rounded-tl-2xl"></div>
          <div class="absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 border-amber-500 rounded-tr-2xl"></div>
          <div class="absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 border-amber-500 rounded-bl-2xl"></div>
          <div class="absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 border-amber-500 rounded-br-2xl"></div>
        </div>
      </div>

      <div class="p-10 bg-gradient-to-t from-black/90 to-transparent flex justify-center items-center pb-safe">
        <button @click="tomarFoto" class="w-20 h-20 bg-transparent rounded-full border-[6px] border-amber-500 flex items-center justify-center active:scale-95 transition-transform group">
          <div class="w-14 h-14 bg-amber-500 rounded-full group-active:bg-amber-400"></div>
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const video = ref(null);
const canvas = ref(null);
const mostrarCamara = ref(false); 
const nuevoMensaje = ref(''); 

const mostrarBotonScroll = ref(false);

const editandoId = ref(null);
const textoEditado = ref("");
const idFotoAEditar = ref(null);

// Variables del Modal de Confirmación
const mostrarModalConfirmacion = ref(false);
const idEventoAEliminar = ref(null);

const eventos = ref([]); 
const orden = ref(null); 
const route = useRoute();
const router = useRouter();

const isRecording = ref(false);
let mediaRecorder = null;
let audioChunks = [];
let pollingInterval = null; 

const textoTranscrito = ref("");
const ORDEN_TRABAJO_ID = route.params.id;

const cotizaciones = ref([]);
const mostrarModalCotizacion = ref(false);
const itemsCotizacion = ref([{ descripcion: '', precio: '' }]);
const contextoCotizacion = ref('');
const fotoEvidencia = ref(null);
const fotoPreview = ref(null);
const enviandoCotizacion = ref(false);

const mostrarModalCierre = ref(false);
const itemsCierre = ref([{ descripcion: '', precio: '' }]);
const cerrandoOrden = ref(false);

const cotizacionPendiente = computed(() => cotizaciones.value.find(c => c.estado === 'pendiente') || null);

const totalCierre = computed(() => {
  const aprobadas = cotizaciones.value.filter(c => c.estado === 'aprobada');
  const deCotizaciones = aprobadas.reduce((s, c) => s + c.total, 0);
  const extra = itemsCierre.value.reduce((s, i) => s + (parseFloat(i.precio) || 0), 0);
  return deCotizaciones + extra;
});

const esMensajeCliente = (texto) => texto && (texto.includes('Mensaje del Cliente:') || texto.includes('💬'));
const limpiarMensajeCliente = (texto) => texto?.replace(/💬?\s*Mensaje del Cliente:\s*/, '').trim() || '';

const esCotizacionEnviada = (texto) => texto?.startsWith('💰');
const esCotizacionAprobada = (texto) => texto?.startsWith('✅ Cliente aprobó');
const esCotizacionRechazada = (texto) => texto?.startsWith('❌ Cliente rechazó');
const esCotizacionEvento = (texto) => esCotizacionEnviada(texto) || esCotizacionAprobada(texto) || esCotizacionRechazada(texto);

const parsearCotizacionEnviada = (texto) => {
  const match = texto?.match(/💰 Cotización enviada al cliente por \$([0-9.]+): (.+)/s);
  return match ? { total: match[1], contexto: match[2] } : { total: '0', contexto: texto };
};

const obtenerUrlImagen = (rutaImagen) => {
  if (!rutaImagen) return '';

  const apiUrl = import.meta.env.VITE_API_URL;
  const baseUrl = apiUrl.replace('/api', '');

  if (rutaImagen.startsWith('http')) {
    try {
      const urlObj = new URL(rutaImagen);
      return `${baseUrl}${urlObj.pathname}`;
    } catch (e) {
      return rutaImagen;
    }
  }

  return `${baseUrl}${rutaImagen}`;
};

const irAlMenuPrincipal = () => {
  router.push('/'); 
};

const scrollToBottom = () => {
  window.scrollTo({
    top: document.documentElement.scrollHeight,
    behavior: 'smooth'
  });
};

const manejarScroll = () => {
  const alturaTotal = document.documentElement.scrollHeight;
  const alturaVentana = window.innerHeight;
  const posicionScroll = window.scrollY;
  mostrarBotonScroll.value = (alturaTotal - (posicionScroll + alturaVentana)) > 150;
};

// --- LOGICA MODAL ELIMINAR EVENTOS ---
const confirmarEliminacion = (id) => {
  idEventoAEliminar.value = id;
  mostrarModalConfirmacion.value = true;
};

const ejecutarEliminacion = async () => {
  if (!idEventoAEliminar.value) return;
  
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/muro/${idEventoAEliminar.value}/`, { 
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    });
    if (response.ok) {
      eventos.value = eventos.value.filter(e => e.id !== idEventoAEliminar.value);
    } else {
      alert("No se pudo eliminar el registro.");
    }
  } catch (error) {
    console.error("Error al eliminar:", error);
  } finally {
    mostrarModalConfirmacion.value = false;
    idEventoAEliminar.value = null;
  }
};

const cancelarEliminacion = () => {
  mostrarModalConfirmacion.value = false;
  idEventoAEliminar.value = null;
};
// ------------------------------------

const iniciarEdicionTexto = (evento) => {
  editandoId.value = evento.id;
  textoEditado.value = evento.contenido_texto;
};

const cancelarEdicion = () => {
  editandoId.value = null;
  textoEditado.value = "";
};

const guardarEdicionTexto = async (evento) => {
  if (!textoEditado.value.trim()) {
    alert("El texto no puede estar vacío. Usa el botón de eliminar si deseas borrarlo.");
    return;
  }
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/muro/${evento.id}/`, {
      method: 'PATCH',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({ contenido_texto: textoEditado.value.trim() })
    });
    if (response.ok) {
      const eventoActualizado = await response.json();
      const index = eventos.value.findIndex(e => e.id === evento.id);
      if (index !== -1) eventos.value[index] = eventoActualizado;
      cancelarEdicion();
    }
  } catch (error) {
    console.error("Error al guardar edición:", error);
  }
};

const abrirCamara = async (idAEditar = null) => {
  idFotoAEditar.value = typeof idAEditar === 'number' ? idAEditar : null;
  mostrarCamara.value = true;
  try {
    const constraints = { video: { facingMode: { ideal: 'environment' } } };
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    video.value.srcObject = stream;
  } catch (error) {
    console.error("Error al acceder a la cámara:", error);
    try {
        const streamGenerico = await navigator.mediaDevices.getUserMedia({ video: true });
        video.value.srcObject = streamGenerico;
    } catch (segundoError) {
        alert("No se encontró ninguna cámara.");
        mostrarCamara.value = false;
    }
  }
};

const cerrarCamara = () => {
  if (video.value && video.value.srcObject) {
    video.value.srcObject.getTracks().forEach(track => track.stop());
  }
  mostrarCamara.value = false;
  idFotoAEditar.value = null;
};

const tomarFoto = () => {
  if (!video.value || !canvas.value) return;
  const context = canvas.value.getContext('2d');
  canvas.value.width = video.value.videoWidth;
  canvas.value.height = video.value.videoHeight;
  context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height);
  
  canvas.value.toBlob((blob) => {
    subirFotoADjango(blob);
    cerrarCamara(); 
  }, 'image/jpeg', 0.8);
};

const subirFotoADjango = async (blob) => {
  const formData = new FormData();
  formData.append('archivo', blob, `evidencia_${Date.now()}.jpg`);
  
  let url = `${import.meta.env.VITE_API_URL}/muro/`;
  let method = 'POST';

  if (idFotoAEditar.value) {
    url = `${import.meta.env.VITE_API_URL}/muro/${idFotoAEditar.value}/`;
    method = 'PATCH';
  } else {
    formData.append('orden', ORDEN_TRABAJO_ID);
    formData.append('tipo', 'foto');
  }

  try {
    const response = await fetch(url, { 
      method, 
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
      body: formData 
    });
    if (response.ok) {
      const data = await response.json();
      if (idFotoAEditar.value) {
        const index = eventos.value.findIndex(e => e.id === idFotoAEditar.value);
        if (index !== -1) eventos.value[index] = data;
      } else {
        eventos.value.push(data);
        await nextTick();
        scrollToBottom();
      }
    }
  } catch (error) {
    console.error('Error de red al subir foto:', error);
  } finally {
    idFotoAEditar.value = null;
  }
};

const irAWhatsApp = () => {
  if (orden.value && orden.value.celular_cliente) {
    window.open(`https://wa.me/${orden.value.celular_cliente}`, '_blank');
  } else {
    alert("El número de celular del cliente no está disponible.");
  }
};

const enviarNota = async () => {
  const texto = nuevoMensaje.value.trim();
  if (!texto) return;

  nuevoMensaje.value = '';

  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/muro/`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        orden: ORDEN_TRABAJO_ID,
        tipo: 'nota',
        contenido_texto: texto
      })
    });

    if (response.ok) {
      const data = await response.json();
      eventos.value.push(data); 
      await nextTick();
      scrollToBottom();
    }
  } catch (error) {
    console.error("Error al enviar nota:", error);
  }
};

const cargarDatosOrden = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/ordenes/${ORDEN_TRABAJO_ID}/`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    });
    if (response.ok) {
      orden.value = await response.json();
    }
  } catch (error) {
    console.error("Error cargando los detalles:", error);
  }
};

const esNuevoDia = (index) => {
  if (index === 0) return true;
  const fechaActual = new Date(eventos.value[index].fecha).toDateString();
  const fechaAnterior = new Date(eventos.value[index - 1].fecha).toDateString();
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

const abrirModalCierre = () => {
  itemsCierre.value = [{ descripcion: '', precio: '' }];
  mostrarModalCierre.value = true;
};

const eliminarItemCierre = (index) => {
  if (itemsCierre.value.length > 1) itemsCierre.value.splice(index, 1);
};

const confirmarCierre = async () => {
  cerrandoOrden.value = true;
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/motos/finalizar/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
      body: JSON.stringify({ orden_id: ORDEN_TRABAJO_ID, total_cobro: totalCierre.value }),
    });
    if (response.ok) {
      mostrarModalCierre.value = false;
      cargarMuro(true);
      cargarDatosOrden();
    } else {
      const resData = await response.json();
      alert('Error: ' + (resData.error || 'Desconocido'));
    }
  } catch {
    alert('Problema conectando con el servidor.');
  } finally {
    cerrandoOrden.value = false;
  }
};

const toggleRecording = () => {
  isRecording.value ? stopRecording() : startRecording();
};

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', audioBlob, 'grabacion.webm'); 
      formData.append('orden_id', ORDEN_TRABAJO_ID); 

      try {
        textoTranscrito.value = "IA procesando audio... ⏳"; 
        const respuesta = await fetch(`${import.meta.env.VITE_API_URL}/muro/audio/`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
          body: formData, 
        });
        const data = await respuesta.json();

        if (respuesta.ok) {
          textoTranscrito.value = data.transcripcion;
          
          if (data.eventos_guardados && data.eventos_guardados.length > 0) {
            data.eventos_guardados.forEach(evento => {
              eventos.value.push(evento);
            });
            await nextTick();
            scrollToBottom();
          } else {
            await cargarMuro(true);
          }

          setTimeout(() => { textoTranscrito.value = ""; }, 5000); 
        } else {
          textoTranscrito.value = "Error: " + (data.error || data.detalle);
        }
      } catch (error) {
        textoTranscrito.value = "Error de conexión.";
      }
    };
    mediaRecorder.start();
    isRecording.value = true;
  } catch (error) {
    alert("Permite el acceso al micrófono.");
  }
};

const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
    isRecording.value = false;
    mediaRecorder.stream.getTracks().forEach(track => track.stop());
  }
};

const actualizarEstadoTarea = async (evento) => {
  try {
    await fetch(`${import.meta.env.VITE_API_URL}/muro/${evento.id}/`, {
      method: 'PATCH',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({ completada: evento.completada })
    });
  } catch (error) {
    console.error("Error al actualizar la tarea:", error);
  }
};

const cargarMuro = async (esCargaInicial = false) => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/muro/?orden=${ORDEN_TRABAJO_ID}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    });
    if (response.ok) {
      const data = await response.json();
      data.sort((a, b) => a.id - b.id);
      eventos.value = data; 
      
      if (esCargaInicial) {
        await nextTick();
        scrollToBottom();
      }
    }
  } catch (error) {
    console.error('Fallo silencioso en el polling:', error);
  }
};

const totalCotizacion = computed(() =>
  itemsCotizacion.value.reduce((sum, item) => sum + (parseFloat(item.precio) || 0), 0)
);

const cargarCotizacion = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/cotizacion/${ORDEN_TRABAJO_ID}/`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
    });
    if (response.ok) cotizaciones.value = await response.json();
  } catch (error) {
    console.error('Error cargando cotización:', error);
  }
};

const abrirModalCotizacion = () => {
  itemsCotizacion.value = [{ descripcion: '', precio: '' }];
  contextoCotizacion.value = '';
  fotoEvidencia.value = null;
  fotoPreview.value = null;
  mostrarModalCotizacion.value = true;
};

const onFotoSeleccionada = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  fotoEvidencia.value = file;
  fotoPreview.value = URL.createObjectURL(file);
};

const agregarItem = () => itemsCotizacion.value.push({ descripcion: '', precio: '' });

const eliminarItem = (index) => {
  if (itemsCotizacion.value.length > 1) itemsCotizacion.value.splice(index, 1);
};

const enviarCotizacion = async () => {
  const itemsValidos = itemsCotizacion.value.filter(i => i.descripcion.trim() && parseFloat(i.precio) > 0);
  if (!contextoCotizacion.value.trim()) {
    alert('Describe qué se encontró o por qué se necesita la autorización.');
    return;
  }
  if (itemsValidos.length === 0) {
    alert('Agrega al menos un ítem con descripción y precio válido.');
    return;
  }
  enviandoCotizacion.value = true;
  try {
    const formData = new FormData();
    formData.append('orden_id', ORDEN_TRABAJO_ID);
    formData.append('contexto', contextoCotizacion.value.trim());
    formData.append('items', JSON.stringify(itemsValidos.map(i => ({ descripcion: i.descripcion.trim(), precio: parseFloat(i.precio) }))));
    if (fotoEvidencia.value) formData.append('foto_evidencia', fotoEvidencia.value);

    const response = await fetch(`${import.meta.env.VITE_API_URL}/cotizacion/crear/`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
      body: formData
    });
    if (response.ok) {
      mostrarModalCotizacion.value = false;
      await cargarCotizacion();
      await cargarMuro(false);
    } else {
      alert('Error al enviar la cotización.');
    }
  } catch (error) {
    alert('Problema de conexión.');
  } finally {
    enviandoCotizacion.value = false;
  }
};

onMounted(() => {
  cargarDatosOrden();
  cargarMuro(true);
  cargarCotizacion();
  window.addEventListener('scroll', manejarScroll);
  pollingInterval = setInterval(() => cargarMuro(false), 10000);
});

onUnmounted(() => {
  window.removeEventListener('scroll', manejarScroll);
  if (pollingInterval) clearInterval(pollingInterval);
  cerrarCamara(); 
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .pb-safe {
    padding-bottom: calc(env(safe-area-inset-bottom) + 1rem);
  }
}
</style>