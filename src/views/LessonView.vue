<script setup lang="ts">
import { ref, computed, watch, nextTick, defineEmits } from 'vue';
import AudioPlayer from '../components/AudioPlayer.vue';
import lessonData from '../data/lessons/l1.json';

const props = defineProps<{
  lesson: any;
}>();

const emit = defineEmits(['back']);
const audioPlayerRef = ref<any>(null);

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
  <div class="lesson-page min-h-screen pb-44">
    <!-- Ambient Background -->
    <div class="fixed inset-0 -z-10 overflow-hidden">
      <div class="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-bl from-blue-400/10 via-indigo-300/5 to-transparent rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-[600px] h-[600px] bg-gradient-to-tr from-violet-400/10 via-pink-300/5 to-transparent rounded-full blur-3xl"></div>
    </div>

    <!-- Header -->
    <header class="sticky top-0 z-30 backdrop-blur-xl bg-white/70 border-b border-gray-100/50">
      <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-5">
          <!-- Back Button -->
          <button 
            @click="emit('back')"
            class="group flex items-center gap-2.5 text-gray-400 hover:text-gray-900 transition-all duration-300"
          >
            <div class="w-9 h-9 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-center group-hover:bg-blue-50 group-hover:border-blue-100 group-hover:scale-105 transition-all duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 group-hover:text-blue-600">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
              </svg>
            </div>
          </button>
          
          <!-- Divider -->
          <div class="h-5 w-px bg-gray-200"></div>

          <!-- Title Area -->
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="white" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-black tracking-tight text-gray-900">{{ lesson?.id === 'l1' ? lessonData.title : lesson.subtitle }}</h1>
              <p class="text-xs text-gray-400 font-medium">New Concept English</p>
            </div>
          </div>
        </div>
        
        <!-- Badge -->
        <div class="hidden md:flex items-center gap-3">
          <div class="flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-full border border-blue-100/50">
            <div class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></div>
            <span class="text-[10px] font-bold text-blue-600 uppercase tracking-wider">Visual NCE</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="max-w-6xl mx-auto px-6 py-10">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
        
        <!-- Left: Scene Viewer (Sticky) -->
        <div class="lg:col-span-5 lg:sticky lg:top-24 lg:self-start">
          <div class="relative group">
            <!-- Image Container -->
            <div class="aspect-[4/3] bg-gradient-to-br from-slate-100 to-slate-50 rounded-3xl overflow-hidden shadow-2xl shadow-slate-200/50 ring-1 ring-black/5">
              <Transition name="fade" mode="out-in">
                <img 
                  :key="currentImage"
                  :src="currentImage" 
                  :alt="lessonData.title"
                  class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-[1.02]"
                  @error="handleImageError"
                />
              </Transition>
              
              <!-- Scene Badge -->
              <div class="absolute top-4 left-4">
                <div class="backdrop-blur-xl bg-black/40 px-3 py-1.5 rounded-full flex items-center gap-2">
                  <div class="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></div>
                  <span class="text-[10px] font-bold text-white uppercase tracking-wider">
                    Scene {{ activeSegmentId?.replace('s', '') || '1' }}
                  </span>
                </div>
              </div>
              
              <!-- Progress Indicator -->
              <div class="absolute bottom-0 left-0 right-0 h-1 bg-black/10">
                <div 
                  class="h-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-300"
                  :style="{ width: `${(lessonData.segments.findIndex(s => s.id === activeSegmentId) + 1) / lessonData.segments.length * 100}%` }"
                ></div>
              </div>
            </div>
            
            <!-- Glow Effect -->
            <div class="absolute -inset-4 bg-gradient-to-r from-blue-500/20 via-indigo-500/20 to-violet-500/20 rounded-[2rem] blur-2xl opacity-0 group-hover:opacity-60 transition-opacity duration-700 -z-10"></div>
          </div>
          
          <!-- Scene Info -->
          <div class="mt-6 flex items-center justify-between px-1">
            <div class="flex items-center gap-3">
              <div class="flex -space-x-1">
                <div class="w-6 h-6 rounded-full bg-blue-500 ring-2 ring-white flex items-center justify-center text-[8px] font-bold text-white">M</div>
                <div class="w-6 h-6 rounded-full bg-indigo-500 ring-2 ring-white flex items-center justify-center text-[8px] font-bold text-white">W</div>
              </div>
              <span class="text-xs text-gray-500 font-medium">2 speakers</span>
            </div>
            <span class="text-xs text-gray-400 font-mono">{{ lessonData.segments.length }} segments</span>
          </div>
        </div>

        <!-- Right: Script Timeline -->
        <div class="lg:col-span-7">
          <!-- Section Title -->
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-gray-100 to-gray-50 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 text-gray-600">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
                </svg>
              </div>
              <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wide">Dialogue Script</h2>
            </div>
            <p class="text-xs text-gray-400">Click to play</p>
          </div>

          <!-- Script Cards -->
          <div class="space-y-3">
            <div 
              v-for="(s, index) in lessonData.segments" 
              :key="s.id"
              :id="`segment-${s.id}`"
              class="script-card group relative cursor-pointer"
              @click="audioPlayerRef?.playAt(s.startTime)"
            >
              <div 
                class="relative p-5 rounded-2xl transition-all duration-300 border"
                :class="[
                  activeSegmentId === s.id 
                    ? 'bg-white shadow-xl shadow-blue-500/5 border-blue-100 scale-[1.01]' 
                    : 'bg-white/50 border-transparent hover:bg-white hover:shadow-lg hover:border-gray-100'
                ]"
              >
                <div class="flex items-start gap-4">
                  <!-- Avatar -->
                  <div 
                    class="flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center text-xs font-bold shadow-sm transition-transform duration-300 group-hover:scale-110"
                    :class="s.role === 'Man' 
                      ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white' 
                      : 'bg-gradient-to-br from-indigo-500 to-violet-600 text-white'"
                  >
                    {{ s.role[0] }}
                  </div>
                  
                  <!-- Content -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 mb-1.5">
                      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wide">{{ s.role }}</span>
                      <span class="text-[10px] text-gray-300">•</span>
                      <span class="text-[10px] text-gray-400 font-mono">{{ s.startTime.toFixed(1) }}s</span>
                    </div>
                    <p 
                      class="text-base leading-relaxed transition-colors duration-300"
                      :class="activeSegmentId === s.id ? 'text-gray-900 font-semibold' : 'text-gray-600'"
                    >
                      {{ s.text }}
                    </p>
                  </div>
                  
                  <!-- Play Indicator -->
                  <div 
                    class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300"
                    :class="activeSegmentId === s.id 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-gray-100 text-gray-400 opacity-0 group-hover:opacity-100'"
                  >
                    <svg v-if="activeSegmentId !== s.id" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5">
                      <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
                    </svg>
                    <div v-else class="flex gap-0.5 items-end h-3">
                      <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_infinite]"></div>
                      <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.2s_infinite]"></div>
                      <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.4s_infinite]"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Floating Audio Player -->
    <div class="fixed bottom-6 left-0 right-0 z-40 px-6">
      <div class="max-w-2xl mx-auto">
        <AudioPlayer 
          ref="audioPlayerRef"
          :src="lessonData.audio" 
          @timeupdate="handleTimeUpdate"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.lesson-page {
  background: linear-gradient(to bottom, #fafbfc, #f5f7fa);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.script-card {
  -webkit-tap-highlight-color: transparent;
}

@keyframes eq {
  0%, 100% { height: 4px; }
  50% { height: 12px; }
}
</style>
