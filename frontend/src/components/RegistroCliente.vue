<template>
  <div class="min-h-screen bg-zinc-950 p-4 flex flex-col items-center justify-center font-sans">
    <div class="bg-zinc-900 p-6 rounded-2xl border border-zinc-800 w-full max-w-md relative min-h-[450px] flex flex-col shadow-2xl">
      
      <div class="flex items-center justify-between mb-8">
        <button @click="manejarRetroceso" class="text-zinc-500 hover:text-zinc-300 transition-colors p-2 -ml-2 rounded-lg active:bg-zinc-800">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
        </button>
        <div class="flex-1 text-center">
          <h1 class="text-2xl font-black text-zinc-100 uppercase tracking-tight">
            {{ vistaActual === 'inicio' ? nombreTaller : (vistaActual === 'camara' ? 'Escanear Placa' : 'Datos de Ingreso') }}
          </h1>
          <p v-if="vistaActual === 'inicio'" class="text-zinc-500 font-medium text-[10px] tracking-widest mt-1">RECEPCIÓN DE VEHÍCULOS</p>
        </div>
        <div class="w-10"></div> 
      </div>

      <div v-if="vistaActual === 'inicio'" class="flex flex-col gap-5 flex-1 justify-center pb-8">
        <button 
          @click="iniciarEscaneo"
          class="w-full bg-zinc-800 hover:bg-zinc-700 active:bg-zinc-600 border border-zinc-700 text-zinc-100 py-8 px-4 rounded-xl flex flex-col items-center justify-center gap-3 transition-all group shadow-md"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 text-amber-500 group-hover:scale-110 transition-transform">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
          </svg>
          <span class="text-lg font-black tracking-wide uppercase">Buscar Moto Registrada</span>
          <span class="text-xs font-bold text-amber-500/80 bg-amber-500/10 px-2 py-1 rounded">Ingreso rápido con IA</span>
        </button>

        <button 
          @click="iniciarRegistroNuevo"
          class="w-full bg-zinc-950 hover:bg-zinc-900 active:bg-zinc-800 border border-zinc-800 text-zinc-300 py-6 px-4 rounded-xl flex flex-col items-center justify-center gap-3 transition-all"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 text-zinc-500">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m3.75 9v6m3-3H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
          </svg>
          <span class="text-sm font-bold tracking-wide uppercase">Ingreso Manual</span>
        </button>
      </div>

      <div v-if="vistaActual === 'camara'" class="flex flex-col items-center flex-1 justify-center">

        <div class="w-full relative rounded-xl overflow-hidden border-2 border-amber-500 shadow-[0_0_15px_rgba(245,158,11,0.15)] bg-black">
          
          <video ref="videoRef" class="w-full h-72 object-cover opacity-90" autoplay playsinline></video>

          <div class="absolute inset-0 border-[40px] border-black/40 pointer-events-none">
            <div class="w-full h-full border-2 border-dashed border-amber-500/50"></div>
          </div>

        </div>

        <!-- BOTÓN FUERA DEL RECUADRO -->
        <div class="mt-5 flex justify-center w-full">
          <button
            @click="tomarFotoYProcesar"
            class="bg-amber-500 hover:bg-amber-400 active:scale-95 text-zinc-950 px-8 py-3.5 rounded-lg font-black shadow-lg text-sm uppercase tracking-widest flex items-center gap-2 transition-all"
            :disabled="procesando"
          >
            <svg
              v-if="!procesando"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="2.5"
              stroke="currentColor"
              class="w-5 h-5"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
            </svg>

            <div v-else class="animate-spin rounded-full h-5 w-5 border-b-2 border-zinc-950"></div>

            {{ procesando ? 'Procesando...' : 'Capturar Placa' }}
          </button>
        </div>

        <p
          v-if="mensajeIA"
          class="mt-6 text-xs font-bold uppercase tracking-widest text-center text-amber-500 animate-pulse bg-amber-500/10 px-4 py-2 rounded"
        >
          {{ mensajeIA }}
        </p>

      </div>

      <form v-if="vistaActual === 'formulario'" @submit.prevent="registrarIngreso" class="space-y-5 flex-1">
        
        <div v-if="mensajeIA" :class="motoEncontrada ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' : 'bg-amber-500/10 text-amber-500 border-amber-500/30'" class="p-3 rounded-lg border text-xs font-bold text-center uppercase tracking-wide">
          {{ mensajeIA }}
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-1.5 pl-1">Placa Vehicular</label>
          <input v-model="formulario.placa" type="text" required class="block w-full rounded-xl bg-zinc-950 border border-zinc-700 text-zinc-100 p-3.5 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 uppercase font-mono text-xl tracking-widest outline-none transition-all placeholder-zinc-700" placeholder="Ej: JW467F">
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-1.5 pl-1">Modelo / Marca</label>
          <input v-model="formulario.modelo" type="text" required class="block w-full rounded-xl bg-zinc-950 border border-zinc-700 text-zinc-100 p-3.5 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-all placeholder-zinc-700 font-medium" placeholder="Ej: Daytona Scrambler 250">
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-1.5 pl-1">Nombre del Propietario</label>
          <input v-model="formulario.nombre" type="text" required class="block w-full rounded-xl bg-zinc-950 border border-zinc-700 text-zinc-100 p-3.5 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-all placeholder-zinc-700 font-medium" placeholder="Nombre completo">
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-1.5 pl-1">Celular (WhatsApp)</label>
          <input v-model="formulario.celular" type="tel" required class="block w-full rounded-xl bg-zinc-950 border border-zinc-700 text-zinc-100 p-3.5 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 font-mono text-lg outline-none transition-all placeholder-zinc-700" placeholder="09...">
        </div>

        <button type="submit" class="w-full bg-amber-500 hover:bg-amber-400 active:scale-[0.98] text-zinc-950 font-black py-4 px-4 rounded-xl mt-6 transition-all uppercase tracking-widest text-sm shadow-[0_0_15px_rgba(245,158,11,0.15)] flex justify-center items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          Ingresar al Taller
        </button>
      </form>

    </div>

    <canvas ref="canvasRef" class="hidden"></canvas>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const API_URL = import.meta.env.VITE_API_URL;
const nombreTaller = import.meta.env.VITE_NOMBRE_TALLER || 'TallerEC';

const vistaActual = ref('inicio');

const formulario = reactive({
  placa: '',
  modelo: '',
  nombre: '',
  celular: ''
});

const videoRef = ref(null);
const canvasRef = ref(null);
let stream = null;
const procesando = ref(false);
const mensajeIA = ref('');
const motoEncontrada = ref(false);

const limpiarFormulario = () => {
  formulario.placa = ''; formulario.modelo = '';
  formulario.nombre = ''; formulario.celular = '';
  mensajeIA.value = ''; motoEncontrada.value = false;
};

// NUEVA LÓGICA DEL BOTÓN ATRÁS
const manejarRetroceso = () => {
  if (vistaActual.value !== 'inicio') {
    // Si estamos en cámara o formulario, volvemos a la selección
    cerrarCamara();
    limpiarFormulario();
    vistaActual.value = 'inicio';
  } else {
    // Si estamos en inicio, regresamos al Tablero Kanban
    router.push('/');
  }
};

const volverInicio = () => {
  cerrarCamara();
  limpiarFormulario();
  vistaActual.value = 'inicio';
};

const iniciarRegistroNuevo = () => {
  limpiarFormulario();
  vistaActual.value = 'formulario';
};

const iniciarEscaneo = async () => {
  limpiarFormulario();
  vistaActual.value = 'camara';
  try {
    stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: { ideal: 'environment' } } 
    });
    setTimeout(() => {
      if (videoRef.value) videoRef.value.srcObject = stream;
    }, 100);
  } catch (error) {
    alert("No se pudo acceder a la cámara.");
    volverInicio();
  }
};

const cerrarCamara = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
};

const tomarFotoYProcesar = async () => {
  if (!videoRef.value || !canvasRef.value) return;
  
  procesando.value = true;
  mensajeIA.value = 'Leyendo placa con IA...';

  const video = videoRef.value;
  const canvas = canvasRef.value;
  
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);

  canvas.toBlob(async (blob) => {
    const formData = new FormData();
    formData.append('imagen', blob, 'placa.jpg');

    try {
      const response = await fetch(`${API_URL}/motos/escanear/`, { 
        method: 'POST', 
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
        body: formData 
      });
      const data = await response.json();

      if (!response.ok) throw new Error(data.error || 'Error leyendo placa');

      formulario.placa = data.placa;
      mensajeIA.value = data.mensaje;
      motoEncontrada.value = data.existe;

      if (data.existe && data.datos) {
        formulario.modelo = data.datos.modelo || '';
        formulario.nombre = data.datos.nombre || '';
        formulario.celular = data.datos.celular || '';
      }

      cerrarCamara();
      vistaActual.value = 'formulario';

    } catch (error) {
      mensajeIA.value = `Error: ${error.message}`;
    } finally {
      procesando.value = false;
    }
  }, 'image/jpeg');
};

const registrarIngreso = async () => {
  try {
    const response = await fetch(`${API_URL}/motos/registrar/`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify(formulario)
    });

    if (response.ok) {
      const data = await response.json();
      router.push(`/muro/${data.orden_id}`);
    } else {
      const resData = await response.json();
      alert("Error al registrar: " + (resData.error || "Desconocido"));
    }
  } catch (error) {
    console.error("Error de red:", error);
  }
};
</script>