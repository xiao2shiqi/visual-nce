<script setup lang="ts">
import { ref, computed, watch, nextTick, defineEmits } from 'vue';
import AudioPlayer from '../components/AudioPlayer.vue';
import lessonData from '../data/lessons/l1.json';

const emit = defineEmits(['back']);

const currentTime = ref(0);

// 计算当前活跃的片段 ID
const activeSegmentId = computed(() => {
  const segment = lessonData.segments.find(
    (s) => currentTime.value >= s.startTime && currentTime.value <= s.endTime
  );
  return segment ? segment.id : null;
});

// 计算当前应显示的图片
const currentImage = computed(() => {
  const segment = lessonData.segments.find(
    (s) => currentTime.value >= s.startTime && currentTime.value <= s.endTime
  );
  
  if (segment && segment.image) return segment.image;
  
  // 保持显示最后一张匹配的图片，避免空白
  const pastSegments = lessonData.segments.filter(s => s.startTime <= currentTime.value);
  if (pastSegments.length > 0) {
    const lastImg = pastSegments[pastSegments.length - 1].image;
    if (lastImg) return lastImg;
  }
  
  return lessonData.segments[0].image;
});

// 处理图片加载失败
const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement;
  console.error('Image load failed:', img.src);
  // 如果加载失败，可以尝试设置一个占位图或记录日志
};


const handleTimeUpdate = (time: number) => {
  currentTime.value = time;
};

// 监听活跃片段变化，自动滚动
watch(activeSegmentId, async (newId) => {
  if (newId) {
    await nextTick();
    scrollToActive(newId);
  }
});

const scrollToActive = (id: string) => {
  const el = document.getElementById(`segment-${id}`);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
};
</script>

<template>
  <div class="min-h-screen pb-40">
    <!-- Header -->
    <header class="glass sticky top-0 z-30 shadow-sm transition-all duration-300">
      <div class="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
        <div class="flex items-center gap-6">
          <button 
            @click="emit('back')"
            class="group flex items-center gap-2 text-gray-400 hover:text-blue-600 transition-colors duration-300"
          >
            <div class="w-8 h-8 rounded-full border border-gray-200 flex items-center justify-center group-hover:border-blue-200 group-hover:bg-blue-50 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
              </svg>
            </div>
            <span class="text-sm font-bold uppercase tracking-widest hidden sm:inline">Back</span>
          </button>
          
          <div class="h-6 w-px bg-gray-200 hidden sm:block"></div>

          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="white" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z" />
              </svg>
            </div>
            <h1 class="text-2xl font-black tracking-tight text-gray-900">{{ lessonData.title }}</h1>
          </div>
        </div>
        <div class="hidden md:flex items-center gap-4">
          <div class="px-4 py-1.5 glass rounded-full text-xs font-bold text-blue-600 border-blue-100 uppercase tracking-widest shadow-sm">
            Visual NCE
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-6xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-2 gap-10 mt-6 lg:items-start">
      
      <!-- Left Column: Visual Scene (Sticky) -->
      <div class="lg:sticky lg:top-28 space-y-6">
        <div class="relative group">
          <!-- Main Image Container -->
          <div class="aspect-video bg-gray-200 rounded-[2rem] overflow-hidden shadow-2xl ring-1 ring-white transition-all duration-500 group-hover:shadow-blue-500/10">
            <Transition name="fade" mode="out-in">
              <img 
                :key="currentImage"
                :src="currentImage" 
                :alt="lessonData.title"
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
            </Transition>
            
            <!-- Image Info Overlay -->
            <div class="absolute bottom-4 left-4 right-4 flex justify-between items-end pointer-events-none">
              <div class="glass px-3 py-1 rounded-lg text-[10px] font-bold text-gray-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                SCENE PREVIEW
              </div>
            </div>
          </div>
          
          <!-- Decorative element behind image -->
          <div class="absolute -inset-2 bg-gradient-to-tr from-blue-500/10 to-purple-500/10 -z-10 blur-2xl rounded-[3rem] opacity-50"></div>
        </div>

        <div class="flex items-center justify-between px-2">
           <div class="flex items-center gap-2">
             <div class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
             <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider">
               Scene: <span class="text-gray-900">{{ currentImage.split('/').pop()?.split('.')[0] }}</span>
             </p>
           </div>
           <div class="text-xs font-mono text-gray-400 bg-gray-100 px-2 py-1 rounded">
             {{ currentTime.toFixed(1) }} / Total
           </div>
        </div>
      </div>

      <!-- Right Column: Interactive Script -->
      <div class="space-y-4 pb-20">
        <div 
          v-for="s in lessonData.segments" 
          :key="s.id"
          :id="`segment-${s.id}`"
          class="group relative p-6 rounded-2xl transition-all duration-300 border border-transparent cursor-pointer"
          :class="[
            activeSegmentId === s.id 
              ? 'bg-white shadow-xl shadow-blue-900/5 ring-1 ring-blue-500/10 scale-[1.02] z-10' 
              : 'hover:bg-white/60 hover:shadow-lg'
          ]"
          @click="currentTime = s.startTime" 
        >
          <!-- Active Indicator Line -->
          <div 
            class="absolute left-0 top-6 bottom-6 w-1 rounded-full transition-all duration-500"
            :class="activeSegmentId === s.id ? 'bg-blue-600 scale-y-100' : 'bg-transparent scale-y-0 text-white'"
          ></div>

          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-3">
              <span 
                class="text-[10px] font-black px-2.5 py-1 rounded-lg tracking-wider"
                :class="s.role === 'Man' 
                  ? 'bg-blue-50 text-blue-600 border border-blue-100' 
                  : 'bg-pink-50 text-pink-500 border border-pink-100'"
              >
                {{ s.role.toUpperCase() }}
              </span>
              <span class="text-[10px] text-gray-400 font-bold font-mono tracking-tighter transition-opacity duration-300"
                :class="activeSegmentId === s.id ? 'opacity-100' : 'opacity-40 group-hover:opacity-80'"
              >
                {{ s.startTime }}S • {{ s.endTime }}S
              </span>
            </div>
            
            <div v-if="activeSegmentId === s.id" class="flex gap-1">
              <div class="w-1 h-3 bg-blue-400 rounded-full animate-[bounce_1s_infinite]"></div>
              <div class="w-1 h-3 bg-blue-600 rounded-full animate-[bounce_1.2s_infinite]"></div>
              <div class="w-1 h-3 bg-blue-400 rounded-full animate-[bounce_0.8s_infinite]"></div>
            </div>
          </div>
          
          <p 
            class="text-xl leading-relaxed transition-all duration-300"
            :class="activeSegmentId === s.id ? 'text-gray-900 font-semibold' : 'text-gray-500 font-medium'"
          >
            {{ s.text }}
          </p>
        </div>
      </div>
    </div>

    <!-- Floating Audio Player Container -->
    <div class="fixed bottom-8 left-0 right-0 z-40 px-6">
      <div class="max-w-3xl mx-auto drop-shadow-2xl">
        <AudioPlayer 
          :src="lessonData.audio" 
          @timeupdate="handleTimeUpdate"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease, filter 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  filter: blur(8px);
}

/* Ensure smooth interaction */
.group {
  -webkit-tap-highlight-color: transparent;
}
</style>


