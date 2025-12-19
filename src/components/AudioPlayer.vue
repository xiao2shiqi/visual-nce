<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps<{
  src: string;
}>();

const emit = defineEmits<{
  (e: 'timeupdate', time: number): void;
}>();

const audioRef = ref<HTMLAudioElement | null>(null);
const isPlaying = ref(false);
const currentTime = ref(0);
const duration = ref(0);

const togglePlay = () => {
  if (!audioRef.value) return;
  if (isPlaying.value) {
    audioRef.value.pause();
  } else {
    audioRef.value.play();
  }
};

const onTimeUpdate = () => {
  if (!audioRef.value) return;
  currentTime.value = audioRef.value.currentTime;
  emit('timeupdate', currentTime.value);
};

const onLoadedMetadata = () => {
  if (!audioRef.value) return;
  duration.value = audioRef.value.duration;
};

const onPlay = () => (isPlaying.value = true);
const onPause = () => (isPlaying.value = false);

const seek = (event: MouseEvent) => {
  if (!audioRef.value || !duration.value) return;
  const progressBar = event.currentTarget as HTMLElement;
  const rect = progressBar.getBoundingClientRect();
  const clickX = event.clientX - rect.left;
  const width = rect.width;
  const percentage = clickX / width;
  
  const newTime = percentage * duration.value;
  audioRef.value.currentTime = newTime;
};

// Format time helper (e.g. 65 -> "1:05")
const formatTime = (seconds: number) => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
};

const playAt = (seconds: number) => {
  if (!audioRef.value) return;
  audioRef.value.currentTime = seconds;
  audioRef.value.play();
  isPlaying.value = true;
};

defineExpose({
  playAt
});
</script>

<template>
  <div class="audio-player glass p-5 rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.1)] flex items-center gap-6 border border-white/40">
    <!-- Play/Pause Button -->
    <button 
      @click="togglePlay"
      class="w-14 h-14 flex-shrink-0 flex items-center justify-center bg-gradient-to-br from-blue-600 to-indigo-700 text-white rounded-2xl hover:scale-105 transition-all shadow-lg shadow-blue-500/40 active:scale-95 group relative overflow-hidden"
    >
      <div class="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
      <span v-if="!isPlaying" class="relative z-10 scale-125">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
          <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
        </svg>
      </span>
      <span v-else class="relative z-10 scale-125">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
          <path fill-rule="evenodd" d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z" clip-rule="evenodd" />
        </svg>
      </span>
    </button>
    
    <div class="flex-1 min-w-0 py-1">
      <!-- Info Row -->
      <div class="flex justify-between items-end mb-2.5">
        <div class="flex items-center gap-2">
           <div v-if="isPlaying" class="flex gap-0.5 h-3 items-end">
              <div class="w-0.5 bg-blue-500 animate-[bounce_0.8s_infinite]"></div>
              <div class="w-0.5 bg-blue-500 animate-[bounce_1.2s_infinite]"></div>
              <div class="w-0.5 bg-blue-500 animate-[bounce_1s_infinite]"></div>
           </div>
           <span class="text-[10px] font-black tracking-widest text-blue-600/60 uppercase">Playback</span>
        </div>
        <div class="flex gap-1.5 text-[10px] font-bold font-mono">
          <span class="text-gray-900">{{ formatTime(currentTime) }}</span>
          <span class="text-gray-300">/</span>
          <span class="text-gray-400">{{ formatTime(duration) }}</span>
        </div>
      </div>

      <!-- Progress Bar -->
      <div 
        class="h-2 bg-gray-200/50 rounded-full cursor-pointer relative group transition-all hover:h-3"
        @click="seek"
      >
        <!-- Background track -->
        <div class="absolute inset-0 bg-gray-200/50 rounded-full overflow-hidden">
             <!-- Progress Fill -->
            <div 
              class="h-full bg-gradient-to-r from-blue-500 to-indigo-600 relative rounded-full transition-all duration-150 ease-out"
              :style="{ width: (currentTime / duration * 100) + '%' }"
            >
              <!-- Glow -->
              <div class="absolute right-0 top-0 bottom-0 w-4 shadow-[0_0_15px_rgba(59,130,246,0.6)]"></div>
            </div>
        </div>
        
        <!-- Handle on Hover -->
        <div 
          class="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-white border-2 border-blue-600 rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"
          :style="{ left: `calc(${(currentTime / duration * 100)}% - 8px)` }"
        ></div>
      </div>
    </div>

    <!-- Additional Controls placeholder (Volume/Speed) -->
    <div class="hidden sm:flex items-center gap-3 pl-2 border-l border-gray-200/50">
       <button class="p-2 text-gray-400 hover:text-blue-600 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
          </svg>
       </button>
    </div>

    <audio
      ref="audioRef"
      :src="src"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="onLoadedMetadata"
      @play="onPlay"
      @pause="onPause"
    ></audio>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% { transform: scaleY(0.5); }
  50% { transform: scaleY(1.2); }
}
</style>


