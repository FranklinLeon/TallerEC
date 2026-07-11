<template>
  <div class="min-h-screen bg-zinc-950 flex items-center justify-center p-4 font-sans">
    <div class="max-w-md w-full bg-zinc-900 rounded-2xl shadow-xl p-8 border border-zinc-800">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-black text-zinc-100 tracking-tight uppercase">TallerEC</h2>
        <p class="text-zinc-500 font-medium mt-1 tracking-wide text-sm">ACCESO AL TALLER</p>
      </div>
      
      <form @submit.prevent="iniciarSesion" class="space-y-6">
        <div>
          <label class="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-1.5 pl-1">Usuario</label>
          <input 
            v-model="credenciales.username" 
            type="text" 
            required
            class="block w-full rounded-xl bg-zinc-950 border border-zinc-700 text-zinc-100 p-3.5 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-all placeholder-zinc-700"
            placeholder="admin"
          >
        </div>
        
        <div>
          <label class="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-1.5 pl-1">Contraseña</label>
          <input 
            v-model="credenciales.password" 
            type="password" 
            required
            class="block w-full rounded-xl bg-zinc-950 border border-zinc-700 text-zinc-100 p-3.5 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-all placeholder-zinc-700"
            placeholder="••••••••"
          >
        </div>

        <div v-if="error" class="bg-red-500/10 text-red-500 border border-red-500/30 p-3 rounded-lg text-xs font-bold text-center uppercase tracking-wide">
          {{ error }}
        </div>

        <button 
          type="submit" 
          class="w-full bg-amber-500 hover:bg-amber-400 active:scale-[0.98] text-zinc-950 font-black py-4 px-4 rounded-xl mt-6 transition-all uppercase tracking-widest text-sm shadow-[0_0_15px_rgba(245,158,11,0.15)] flex justify-center items-center"
        >
          Ingresar
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const error = ref('');
const credenciales = reactive({
  username: '',
  password: ''
});

const iniciarSesion = async () => {
  error.value = '';
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credenciales)
    });

    if (!response.ok) throw new Error('Credenciales incorrectas');

    const data = await response.json();
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    
    router.push('/');
  } catch (e) {
    error.value = e.message;
  }
};
</script>